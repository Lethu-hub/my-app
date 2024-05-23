import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights
from prediction_models import visualize_prediction_models, predict_error, predict_status_code, predict_page_popularity, predict_load
from basic import read_parse_log, analyze_logs, create_visualizations
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
    accuracy_status_code, y_test_status_code, y_pred_status_code = predict_status_code(log_data)
    figs_status_code = visualize_prediction_models(y_test_status_code, y_pred_status_code, 'Status Code Prediction')
    visualizations.extend(figs_status_code)
    st.write(f"Status Code Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")

    # Page Popularity Prediction
    start_time = time.time()
    mse_page, y_test_page, y_pred_page = predict_page_popularity(log_data)
    figs_page_popularity = visualize_prediction_models(y_test_page, y_pred_page, 'Page Popularity Prediction')
    visualizations.extend(figs_page_popularity)
    st.write(f"Page Popularity Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")

    # Load Prediction
    start_time = time.time()
    load_model_accuracy, y_test_load, load_predictions = predict_load(log_data)
    figs_load = visualize_prediction_models(y_test_load, load_predictions, 'Load Prediction')
    visualizations.extend(figs_load)
    st.write(f"Load Prediction Visuals generated in {time.time() - start_time:.2f} seconds.")

    return visualizations

# Get all visualizations
visualizations = get_visualizations(log_data)

# Display a subset of visualizations in a full-width layout
st.header('All Visualizations')

# Create a container for visualizations
cols = st.columns(4)  # Create 4 columns for visualizations

# Display only the first few visualizations
for i, (fig, title) in enumerate(visualizations[:8]):  # Limiting to first 8 for debugging
    with cols[i % 4]:  # Use modulo to distribute visualizations across columns
        st.subheader(title)
        st.pyplot(fig)

# Allow user to load more visualizations
if st.button('Load More Visualizations'):
    for i, (fig, title) in enumerate(visualizations[8:]):  # Load the remaining visualizations
        with cols[i % 4]:
            st.subheader(title)
            st.pyplot(fig)

# Custom Visualizations Section
st.header('Create Your Own Visualizations')

# Allow users to select columns for X and Y axes
x_col = st.selectbox('Select X-axis column', log_data.columns)
y_col = st.selectbox('Select Y-axis column', log_data.columns)

# Allow users to select the type of chart
chart_type = st.selectbox('Select Chart Type', ['Line Chart', 'Bar Chart', 'Scatter Plot', 'Histogram'])

# Generate custom visualization based on user inputs
if st.button('Generate Chart'):
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size as needed
    
    if chart_type == 'Line Chart':
        sns.lineplot(data=log_data, x=x_col, y=y_col, ax=ax)
    elif chart_type == 'Bar Chart':
        sns.barplot(data=log_data, x=x_col, y=y_col, ax=ax)
    elif chart_type == 'Scatter Plot':
        sns.scatterplot(data=log_data, x=x_col, y=y_col, ax=ax)
    elif chart_type == 'Histogram':
        sns.histplot(data=log_data, x=x_col, bins=30, ax=ax)

    st.pyplot(fig)
    
    # Option to save custom visualization
    if st.button('Save Chart to Dashboard'):
        visualizations.append((fig, f'Custom {chart_type}'))

st.markdown('---')

# Add a footer
st.text("Fun Olympics")
