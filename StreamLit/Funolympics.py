import streamlit as st
from datetime import datetime, timedelta
from generate_logs import generate_web_logs
from intergration import integrate_csv_files
from preprocessing import read_parse_log
from basic import get_basic_visualizations
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights
from prediction_models import visualize_prediction_models, predict_error, predict_status_code, predict_page_popularity, predict_load

# Set page layout to wide
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Fun Olympics Analytics Dashboard')

# Define start date, end date, and number of logs
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 2)
num_logs = 1000

# Generate web logs
generate_web_logs(start_date, end_date, num_logs, num_files)

# Directory containing the individual log files
input_directory = 'StreamLit/weblogs'

# Output file path
output_file = 'StreamLit/synthetic_web_logs.csv'

# Integrate the CSV files
integrate_csv_files(input_directory, output_file)

# Preprocess logs
output_file = 'StreamLit/preprocessed_web_logs.csv'
read_parse_log(output_file)

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
            visualizations = []

            # Basic Visuals
            basic_visuals = get_basic_visualizations(log_data)
            visualizations.extend(basic_visuals)

            # User Behavior Analysis Visuals
            user_behavior_analysis = analyze_user_behavior(log_data)
            figs_user_behavior = visualize_user_behavior(user_behavior_analysis)
            visualizations.extend(figs_user_behavior)

            # Marketing Insights Visuals
            figs_marketing = visualize_marketing_insights(log_data)
            visualizations.extend(figs_marketing)

            # Prediction Models Visuals
            # Error Prediction
            accuracy_error, y_test_error, y_pred_error = predict_error(log_data)
            figs_error = visualize_prediction_models(y_test_error, y_pred_error, 'Error Prediction')
            visualizations.extend(figs_error)

            # Status Code Prediction
            accuracy_status_code, y_test_status_code, y_pred_status_code = predict_status_code(log_data)
            figs_status_code = visualize_prediction_models(y_test_status_code, y_pred_status_code, 'Status Code Prediction')
            visualizations.extend(figs_status_code)

            # Page Popularity Prediction
            mse_page, y_test_page, y_pred_page = predict_page_popularity(log_data)
            figs_page_popularity = visualize_prediction_models(y_test_page, y_pred_page, 'Page Popularity Prediction')
            visualizations.extend(figs_page_popularity)

            # Load Prediction
            load_model_accuracy, y_test_load, load_predictions = predict_load(log_data)
            figs_load = visualize_prediction_models(y_test_load, load_predictions, 'Load Prediction')
            visualizations.extend(figs_load)

            return visualizations
        except Exception as e:
            st.error(f"Error generating visualizations: {e}")
            return []

    visualizations = get_visualizations(log_data)

    cols = st.columns(4)
    for idx, (fig, title) in enumerate(visualizations):
        with cols[idx % 4]:
            st.subheader(title)
            st.pyplot(fig)

    st.text("Fun Olympics")
else:
    st.error("Failed to load data.")
