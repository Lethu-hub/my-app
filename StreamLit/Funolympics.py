import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from user_behavior import analyze_user_behavior, visualize_user_behavior
from marketing_insights import visualize_marketing_insights, read_parse_log  # Import the read_parse_log function

# Load the preprocessed web logs data
log_data = read_parse_log('StreamLit/preprocessed_web_logs.csv')
log_data['Hour'] = pd.to_datetime(log_data['Timestamp']).dt.hour  # Ensure 'Hour' column is created

# Title of the dashboard
st.title('Web Analytics Dashboard')

# Sidebar selection for different analysis
analysis_choice = st.sidebar.selectbox('Select Analysis', ['User Behavior', 'Marketing Insights', 'Prediction Models', 'Custom Visualizations'])

def get_visualizations(log_data, analysis_type):
    """
    Get the visualizations based on the analysis type.
    
    Args:
    - log_data: DataFrame containing the log data.
    - analysis_type: Type of analysis ('User Behavior', 'Marketing Insights', 'Prediction Models').
    
    Returns:
    - A list of tuples containing (figure, title) for each visualization.
    """
    visualizations = []

    if analysis_type == 'User Behavior':
        user_behavior_analysis = analyze_user_behavior(log_data)
        figs = visualize_user_behavior(user_behavior_analysis)
        visualizations.extend(figs)

    elif analysis_type == 'Marketing Insights':
        figs = visualize_marketing_insights(log_data)
        visualizations.extend(figs)

    elif analysis_type == 'Prediction Models':
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

# Create a section for each type of analysis
if analysis_choice == 'User Behavior':
    st.header('User Behavior Analysis')
elif analysis_choice == 'Marketing Insights':
    st.header('Marketing Insights')
elif analysis_choice == 'Prediction Models':
    st.header('Prediction Models')

visualizations = get_visualizations(log_data, analysis_choice)

# Create a grid container for the thumbnails
for fig, title in visualizations:
    st.subheader(title)
    st.pyplot(fig)
    st.markdown('---')

# Custom Visualizations Section
if analysis_choice == 'Custom Visualizations':
    st.header('Create Your Own Visualizations')

    # Allow users to select columns for X and Y axes
    x_col = st.selectbox('Select X-axis column', log_data.columns)
    y_col = st.selectbox('Select Y-axis column', log_data.columns)

    # Allow users to select the type of chart
    chart_type = st.selectbox('Select Chart Type', ['Line Chart', 'Bar Chart', 'Scatter Plot', 'Histogram'])

    # Generate custom visualization based on user inputs
    if st.button('Generate Chart'):
        fig, ax = plt.subplots()
        
        if chart_type == 'Line Chart':
            sns.lineplot(data=log_data, x=x_col, y=y_col, ax=ax)
        elif chart_type == 'Bar Chart':
            sns.barplot(data=log_data, x=x_col, y=y_col, ax=ax)
        elif chart_type == 'Scatter Plot':
            sns.scatterplot(data=log_data, x=x_col, y=y_col, ax=ax)
        elif chart_type == 'Histogram':
            sns.histplot(data=log_data, x=x_col, bins=30, ax=ax)

        st.pyplot(fig)

# Add a footer
st.text("Fun Olympics")
