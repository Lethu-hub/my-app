import streamlit as st
import pandas as pd
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights
from prediction_models import visualize_prediction_models, predict_error, predict_status_code, predict_page_popularity, predict_load
from basic import read_parse_log

# Set page layout to wide
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Fun Olympics Analytics Dashboard')

# Load the preprocessed web logs data
@st.cache_data
def load_data(file_path):
    try:
        return read_parse_log(file_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

log_data = load_data('StreamLit/preprocessed_web_logs.csv')

if log_data is not None:
    # Sidebar selection for different analysis
    analysis_choice = st.sidebar.selectbox('Select Analysis', ['User Behavior', 'Marketing Insights', 'Prediction Models', 'Custom Visualizations'])

    # Function to get visualizations based on analysis type
    def get_visualizations(log_data, analysis_type):
        try:
            visualizations = []

            if analysis_type == 'User Behavior':
                user_behavior_analysis = analyze_user_behavior(log_data)
                figs = visualize_user_behavior(user_behavior_analysis)
                visualizations.extend(figs)

            elif analysis_type == 'Marketing Insights':
                figs = visualize_marketing_insights(log_data)
                visualizations.extend(figs)

            elif analysis_type == 'Prediction Models':
                accuracy_error, y_test_error, y_pred_error = predict_error(log_data)
                figs_error = visualize_prediction_models(y_test_error, y_pred_error, 'Error Prediction')
                visualizations.extend(figs_error)

                accuracy_status_code, y_test_status_code, y_pred_status_code = predict_status_code(log_data)
                figs_status_code = visualize_prediction_models(y_test_status_code, y_pred_status_code, 'Status Code Prediction')
                visualizations.extend(figs_status_code)

                mse_page, y_test_page, y_pred_page = predict_page_popularity(log_data)
                figs_page_popularity = visualize_prediction_models(y_test_page, y_pred_page, 'Page Popularity Prediction')
                visualizations.extend(figs_page_popularity)

                load_model_accuracy, y_test_load, load_predictions = predict_load(log_data)
                figs_load = visualize_prediction_models(y_test_load, load_predictions, 'Load Prediction')
                visualizations.extend(figs_load)

            return visualizations
        except Exception as e:
            st.error(f"Error generating visualizations: {e}")
            return []

    # Create a section for each type of analysis
    if analysis_choice == 'User Behavior':
        st.header('User Behavior Analysis')
    elif analysis_choice == 'Marketing Insights':
        st.header('Marketing Insights')
    elif analysis_choice == 'Prediction Models':
        st.header('Prediction Models')

    visualizations = get_visualizations(log_data, analysis_choice)

    # Display visualizations side by side
    cols = st.columns(len(visualizations))
    for col, (fig, title) in zip(cols, visualizations):
        with col:
            st.subheader(title)
            st.pyplot(fig)

    # Custom Visualizations Section
    if analysis_choice == 'Custom Visualizations':
        st.header('Create Your Own Visualizations')
        # Your custom visualization code here

    # Add a footer
    st.text("Fun Olympics")
else:
    st.error("Failed to load data.")
