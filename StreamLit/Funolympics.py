import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights
from prediction_models import visualize_prediction_models, predict_error, predict_status_code, predict_page_popularity, predict_load
from basic import read_parse_log, analyze_logs, create_visualizations

# Set page layout to wide
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Fun Olympics Analytics Dashboard')

# Use Streamlit cache to load data
@st.cache_data
def load_data(file_path):
    try:
        start_time = time.time()
        data = read_parse_log(file_path)
        end_time = time.time()
        st.write(f"Data loaded in {end_time - start_time:.2f} seconds.")
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the data
log_data = load_data('StreamLit/preprocessed_web_logs.csv')

if log_data is not None:
    # Function to get visualizations based on analysis type
    def get_visualizations(log_data):
        visualizations = []

        try:
            # Basic Analysis Visuals
            start_time = time.time()
            analysis_results = analyze_logs(log_data)
            figs_basic = create_visualizations(analysis_results)
            visualizations.extend(figs_basic)
            st.write(f"Basic Analysis Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating Basic Analysis Visuals: {e}")

        try:
            # User Behavior Analysis Visuals
            start_time = time.time()
            user_behavior_analysis = analyze_user_behavior(log_data)
            figs_user_behavior = visualize_user_behavior(user_behavior_analysis)
            visualizations.extend(figs_user_behavior)
            st.write(f"User Behavior Analysis Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating User Behavior Analysis Visuals: {e}")

        try:
            # Marketing Insights Visuals
            start_time = time.time()
            figs_marketing = visualize_marketing_insights(log_data)
            visualizations.extend(figs_marketing)
            st.write(f"Marketing Insights Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating Marketing Insights Visuals: {e}")

        try:
            # Prediction Models Visuals
            # Error Prediction
            start_time = time.time()
            accuracy_error, y_test_error, y_pred_error = predict_error(log_data)
            figs_error = visualize_prediction_models(y_test_error, y_pred_error, 'Error Prediction')
            visualizations.extend(figs_error)
            st.write(f"Error Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating Error Prediction Visuals: {e}")

        try:
            # Status Code Prediction
            start_time = time.time()
            accuracy_status_code, y_test_status_code, y_pred_status_code = predict_status_code(log_data)
            figs_status_code = visualize_prediction_models(y_test_status_code, y_pred_status_code, 'Status Code Prediction')
            visualizations.extend(figs_status_code)
            st.write(f"Status Code Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating Status Code Prediction Visuals: {e}")

        try:
            # Page Popularity Prediction
            start_time = time.time()
            mse_page, y_test_page, y_pred_page = predict_page_popularity(log_data)
            figs_page_popularity = visualize_prediction_models(y_test_page, y_pred_page, 'Page Popularity Prediction')
            visualizations.extend(figs_page_popularity)
            st.write(f"Page Popularity Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating Page Popularity Prediction Visuals: {e}")

        try:
            # Load Prediction
            start_time = time.time()
            load_model_accuracy, y_test_load, load_predictions = predict_load(log_data)
            figs_load = visualize_prediction_models(y_test_load, load_predictions, 'Load Prediction')
            visualizations.extend(figs_load)
            st.write(f"Load Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"Error generating Load Prediction Visuals: {e}")

        return visualizations

    # Get all visualizations
    visualizations = get_visualizations(log_data)

    # Display a subset of visualizations in a full-width layout
    st.header('All Visualizations')

    # Create a container for visualizations
    cols = st.columns(4)  # Create 4 columns for visualizations
    for idx, (fig, title) in enumerate(visualizations):
        with cols[idx % 4]:  # Rotate through the columns
            st.pyplot(fig)
            st.write(title)
            plt.close(fig)  # Close the figure after displaying it
else:
    st.error("Failed to load data.")
