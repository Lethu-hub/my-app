import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Function to analyze user behavior
def analyze_user_behavior(log_data):
    log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'])
    log_data['Next Request Time'] = log_data.groupby('IP Address')['Timestamp'].shift(-1)
    log_data['Session Duration'] = (log_data['Next Request Time'] - log_data['Timestamp']).dt.total_seconds() / 60  # in minutes
    
    page_views = log_data['Endpoint'].value_counts().reset_index()
    page_views.columns = ['Endpoint', 'Page Views']
    
    unique_visitors = log_data['IP Address'].nunique()
    
    single_page_visits = log_data['IP Address'].value_counts().eq(1).sum()
    total_visits = log_data['IP Address'].count()
    bounce_rate = (single_page_visits / total_visits) * 100
    
    traffic_sources = log_data['Endpoint'].apply(lambda x: 'Direct' if x == '/index.html' else 'Referral' if 'referral' in x else 'Organic Search')
    traffic_source_counts = traffic_sources.value_counts()
    
    conversion_rate = log_data['Endpoint'].eq('/purchase.html').sum() / total_visits * 100
    
    error_counts = log_data['Status Code'].value_counts()
    
    session_paths = log_data.groupby('IP Address')['Endpoint'].apply(lambda x: ' -> '.join(x)).reset_index()
    
    visit_frequency = log_data.groupby('IP Address')['Timestamp'].count().value_counts().sort_index()
    
    peak_usage_hours = log_data['Hour'].value_counts().sort_index()
    
    exit_pages = log_data.groupby('IP Address')['Endpoint'].apply(lambda x: x.iloc[-1]).value_counts()
    
    form_submission_rates = log_data['Endpoint'].eq('/submit_form.html').mean() * 100
    
    user_behavior_analysis = pd.DataFrame({
        'Metrics': ['Page Views', 'Unique Visitors', 'Session Duration', 'Bounce Rate', 'Traffic Sources', 'Conversion Rate',
                    'Error Analysis', 'Session Paths', 'Frequency of Visits', 'Peak Usage Hours', 'Exit Pages', 
                    'Form Submission Rates'],
        'Results': [page_views, unique_visitors, log_data['Session Duration'].describe(), bounce_rate, traffic_source_counts, 
                    conversion_rate, error_counts, session_paths, visit_frequency, peak_usage_hours, exit_pages,
                    form_submission_rates]
    })
    
    return user_behavior_analysis

# Function to create visualizations
def visualize_user_behavior(user_behavior_analysis):
    figures = []
    
    for index, row in user_behavior_analysis.iterrows():
        metric = row['Metrics']
        result = row['Results']
        
        if metric == 'Page Views':
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Page Views', y='Endpoint', data=result.head(10), ax=ax)
            ax.set_title('Top 10 Pages by Page Views')
            ax.set_xlabel('Page Views')
            ax.set_ylabel('Endpoint')
            figures.append((fig, 'Top 10 Pages by Page Views'))
        
        elif metric == 'Error Analysis':
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=result.index, y=result.values, ax=ax)
            ax.set_title('Error Analysis - Bar Plot')
            ax.set_xlabel('Error Code')
            ax.set_ylabel('Count')
            figures.append((fig, 'Error Analysis - Bar Plot'))

            fig, ax = plt.subplots(figsize=(8, 8))
            result.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
            ax.set_title('Error Analysis - Pie Chart')
            ax.set_ylabel('')
            figures.append((fig, 'Error Analysis - Pie Chart'))
        
        elif metric == 'Peak Usage Hours':
            fig, ax = plt.subplots(figsize=(10, 6))
            result.plot(kind='bar', ax=ax)
            ax.set_title('Peak Usage Hours')
            ax.set_xlabel('Hour')
            ax.set_ylabel('Frequency')
            ax.set_xticklabels(result.index, rotation=45)
            figures.append((fig, 'Peak Usage Hours'))
        
        elif metric == 'Exit Pages':
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=result.values, y=result.index, ax=ax)
            ax.set_title('Exit Pages')
            ax.set_xlabel('Count')
            ax.set_ylabel('Page')
            figures.append((fig, 'Exit Pages'))
    
    return figures

# Example usage
if __name__ == "_main_":
    log_data = pd.read_csv('StreamLit/preprocessed_web_logs.csv')
    log_data['Hour'] = pd.to_datetime(log_data['Timestamp']).dt.hour  # Ensure 'Hour' column is created
    user_behavior_analysis = analyze_user_behavior(log_data)
    visualize_user_behavior(user_behavior_analysis)
