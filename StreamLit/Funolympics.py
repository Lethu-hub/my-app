import streamlit as st
from datetime import datetime
from generate_logs import generate_web_logs
from intergration import integrate_csv_files
from preprocessing import read_parse_log
from basic import get_basic_visualizations
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights
from prediction_models import visualize_prediction_models, predict_error, predict_status_code, predict_page_popularity, predict_load

import matplotlib.pyplot as plt

# Set page layout to wide
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Fun Olympics Analytics Dashboard')

# Define start date, end date, number of logs per file, and number of files
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 2)
num_logs_per_file = 100
num_files = 10

# Generate web logs
st.write("Generating web logs...")
generate_web_logs(start_date, end_date, num_logs_per_file, num_files)
st.write("Web logs generated successfully.")

# Directory containing the individual log files
input_directory = 'StreamLit/weblogs'

# Output file path
output_file = 'StreamLit/synthetic_web_logs.csv'

# Integrate the CSV files
st.write("Integrating CSV files...")
integrate_csv_files(input_directory, output_file)
st.write("CSV files integrated successfully.")

# Preprocess logs
output_file = 'StreamLit/preprocessed_web_logs.csv'
st.write("Preprocessing logs...")
read_parse_log(output_file)
st.write("Logs preprocessed successfully.")

# Load the preprocessed web logs data
@st.cache_data
def load_data(file_path):
    try:
        return read_parse_log(file_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

log_data = load_data(output_file)

if log_data is not None:
    def get_visualizations(log_data):
        try:
            required_visuals = []
            user_behavior_insights = []
            marketing_insights = []
            forecasting_insights = []

            # Basic Visuals
            basic_visuals = get_basic_visualizations(log_data)
            required_visuals.extend(basic_visuals)

            # User Behavior Analysis Visuals
            user_behavior_analysis = analyze_user_behavior(log_data)
            figs_user_behavior = visualize_user_behavior(user_behavior_analysis)
            user_behavior_insights.extend(figs_user_behavior)

            # Marketing Insights Visuals
            figs_marketing = visualize_marketing_insights(log_data)
            marketing_insights.extend(figs_marketing)

            # Prediction Models Visuals
            # Error Prediction
            accuracy_error, y_test_error, y_pred_error = predict_error(log_data)
            figs_error = visualize_prediction_models(y_test_error, y_pred_error, 'Error Prediction')
            forecasting_insights.extend(figs_error)

            # Status Code Prediction
            accuracy_status_code, y_test_status_code, y_pred_status_code = predict_status_code(log_data)
            figs_status_code = visualize_prediction_models(y_test_status_code, y_pred_status_code, 'Status Code Prediction')
            forecasting_insights.extend(figs_status_code)

            # Page Popularity Prediction
            mse_page, y_test_page, y_pred_page = predict_page_popularity(log_data)
            figs_page_popularity = visualize_prediction_models(y_test_page, y_pred_page, 'Page Popularity Prediction')
            forecasting_insights.extend(figs_page_popularity)

            # Load Prediction
            load_model_accuracy, y_test_load, load_predictions = predict_load(log_data)
            figs_load = visualize_prediction_models(y_test_load, load_predictions, 'Load Prediction')
            forecasting_insights.extend(figs_load)

            return {
                'Required Visuals': required_visuals,
                'User Behavior Insights': user_behavior_insights,
                'Marketing Insights': marketing_insights,
                'Forecasting Insights': forecasting_insights
            }
        except Exception as e:
            st.error(f"Error generating visualizations: {e}")
            return {}

    visualizations = get_visualizations(log_data)

    for section, visuals in visualizations.items():
        st.header(section)
        cols = st.columns(4)
        for idx, (fig, title) in enumerate(visuals):
            with cols[idx % 4]:
                st.subheader(title)
                st.pyplot(fig)

    st.text("Fun Olympics")

# Add a form for users to generate and save new visualizations
st.header("Create Visuals")
with st.form(key='create_visuals_form'):
    st.write("Select columns to create visualization:")
    columns = log_data.columns.tolist()
    selected_columns = st.multiselect("Choose columns", columns)

    viz_type = st.selectbox("Select visualization type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])

    submit_button = st.form_submit_button(label='Create Visual')

    if submit_button and selected_columns:
        fig, ax = plt.subplots()
        if viz_type == "Bar Chart":
            log_data[selected_columns].plot(kind='bar', ax=ax)
        elif viz_type == "Line Chart":
            log_data[selected_columns].plot(kind='line', ax=ax)
        elif viz_type == "Scatter Plot":
            if len(selected_columns) == 2:
                log_data.plot(kind='scatter', x=selected_columns[0], y=selected_columns[1], ax=ax)
            else:
                st.error("Scatter plot requires exactly 2 columns.")
                fig = None
        elif viz_type == "Pie Chart":
            if len(selected_columns) == 1:
                log_data[selected_columns[0]].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
            else:
                st.error("Pie chart requires exactly 1 column.")
                fig = None
        elif viz_type == "Histogram":
            log_data[selected_columns].plot(kind='hist', ax=ax, bins=30)
        else:
            fig = None

        if fig:
            st.pyplot(fig)
            save_button = st.button('Save to Dashboard')
            if save_button:
                st.session_state['saved_visuals'] = st.session_state.get('saved_visuals', [])
                st.session_state['saved_visuals'].append((fig, f"{viz_type} of {' and '.join(selected_columns)}"))
                st.success("Visualization saved to Dashboard!")

# Display saved visuals under Custom Visuals
if 'saved_visuals' in st.session_state:
    st.header("Custom Visuals")
    for idx, (fig, title) in enumerate(st.session_state['saved_visuals']):
        st.subheader(f"{idx + 1}. {title}")
        st.pyplot(fig)
else:
    st.error("Failed to load data.")

# Footer
st.text("© Fun Olympics")
