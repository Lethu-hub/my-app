import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights
from prediction_models import visualize_prediction_models, predict_error, predict_status_code, predict_page_popularity, predict_load
from basic import read_parse_log, analyze_logs, create_visualizations  # Import from basic.py
import time

# Set page layout to wide
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Fun Olympics Analytics Dashboard')

# Use Streamlit cache to load data
@st.cache_data
def load_data(file_path):
    start_time = time.time()
    data = read_parse_log(file_path)
    end_time = time.time()
    st.write(f"Data loaded in {end_time - start_time:.2f} seconds.")
    return data

# Load the data
log_data = load_data('StreamLit/preprocessed_web_logs.csv')

# Function to get visualizations based on analysis type
def get_visualizations(log_data):
    visualizations = []

    # Basic Analysis Visuals
    start_time = time.time()
    analysis_results = analyze_logs(log_data)
    figs_basic = create_visualizations(analysis_results)
    visualizations.extend(figs_basic)
    st.write(f"Basic Analysis Visuals generated in {time.time() - start_time:.2f} seconds.")

    # User Behavior Analysis Visuals
    start_time = time.time()
    user_behavior_analysis = analyze_user_behavior(log_data)
    figs_user_behavior = visualize_user_behavior(user_behavior_analysis)
    visualizations.extend(figs_user_behavior)
    st.write(f"User Behavior Analysis Visuals generated in {time.time() - start_time:.2f} seconds.")

    # Marketing Insights Visuals
    start_time = time.time()
    figs_marketing = visualize_marketing_insights(log_data)
    visualizations.extend(figs_marketing)
    st.write(f"Marketing Insights Visuals generated in {time.time() - start_time:.2f} seconds.")

    # Prediction Models Visuals
    # Error Prediction
    start_time = time.time()
    accuracy_error, y_test_error, y_pred_error = predict_error(log_data)
    figs_error = visualize_prediction_models(y_test_error, y_pred_error, 'Error Prediction')
    visualizations.extend(figs_error)
    st.write(f"Error Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")

    # Status Code Prediction
    start_time = time.time()
