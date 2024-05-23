import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read and parse web server log files
def read_parse_log(preprocessed_web_logs):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(preprocessed_web_logs)
    
    # Convert 'Timestamp' column to datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    
    # Extract additional time-related features if needed (e.g., hour of day)
    df['Hour'] = df['Timestamp'].dt.hour
    
    return df

# Function to analyze marketing insights
def analyze_marketing_insights(log_data):
    # Ensure 'Timestamp' column is in datetime format
    log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'], errors='coerce')
    
    # Analyze Traffic Sources Effectiveness
    traffic_sources = log_data['Endpoint'].apply(lambda x: 'Direct' if x == '/index.html' else 'Referral' if 'referral' in x else 'Organic Search')
    traffic_source_counts = traffic_sources.value_counts()

    # Analyze Referral Partnerships
    referral_partners = log_data[log_data['Endpoint'] != '/index.html']['Endpoint'].value_counts().head(3)

    # Analyze Content Performance
    content_performance = log_data['Endpoint'].value_counts()

    # Analyze Seasonal Trends
    seasonal_trends = log_data['Timestamp'].dt.month.value_counts().sort_index()

    return {
        'traffic_source_counts': traffic_source_counts,
        'referral_partners': referral_partners,
        'content_performance': content_performance,
        'seasonal_trends': seasonal_trends
    }

# Function to create visualizations
def visualize_marketing_insights(log_data):
    # Initialize an empty list to store visualizations
    visualizations = []

    # Analyze the marketing insights
    insights = analyze_marketing_insights(log_data)

    # Visualizations for Referral Partnerships
    referral_partners = insights['referral_partners']
    plt.figure(figsize=(10, 6))
    sns.barplot(x=referral_partners.index, y=referral_partners.values)
    plt.title('Top 3 Referral Partnerships')
    plt.xlabel('Referral Partner')
    plt.ylabel('Count')
    plt.tight_layout()
    fig = plt.gcf()
    visualizations.append((fig, 'Top 3 Referral Partnerships'))

    # Visualizations for Content Performance
    content_performance = insights['content_performance']
    plt.figure(figsize=(10, 6))
    sns.barplot(x=content_performance.index, y=content_performance.values)
    plt.title('Content Performance')
    plt.xlabel('Page')
    plt.ylabel('Views')
    plt.tight_layout()
    fig = plt.gcf()
    visualizations.append((fig, 'Content Performance'))

    return visualizations

# Example usage:
if __name__ == "__main__":
    log_data = read_parse_log('preprocessed_web_logs.csv')
    visualizations = visualize_marketing_insights(log_data)
    for fig, title in visualizations:
        fig.show()
