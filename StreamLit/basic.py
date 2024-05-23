import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_parse_log(file_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)
    
    # Split the 'Timestamp' column into separate date and time columns
    split_timestamp = df['Timestamp'].str.split(' ', n=1, expand=True)
    
    # Check if the split was successful
    if len(split_timestamp.columns) == 2:
        df[['Date', 'Time']] = split_timestamp
    else:
        # If split failed, set 'Date' and 'Time' to NaT
        df['Date'] = pd.NaT
        df['Time'] = pd.NaT

    # Extract page information from the endpoint
    df['Page'] = df['Endpoint'].str.extract(r'\/(\w+)\.html$')
    
    # Convert 'Date' and 'Time' columns to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract additional time-related features if needed (e.g., hour of day)
    df['Hour'] = df['Timestamp'].dt.hour
    
    return df

def visualize_country_of_origin(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    country_counts = df['Country'].value_counts()
    sns.barplot(x=country_counts.index, y=country_counts.values, ax=ax)
    ax.set_title('Number of Visits by Country of Origin')
    ax.set_xlabel('Country')
    ax.set_ylabel('Number of Visits')
    plt.xticks(rotation=45)
    return fig, "Country of Origin"

def visualize_number_of_visits(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    visits_per_day = df['Date'].value_counts().sort_index()
    sns.lineplot(x=visits_per_day.index, y=visits_per_day.values, ax=ax)
    ax.set_title('Number of Visits Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Visits')
    plt.xticks(rotation=45)
    return fig, "Number of Visits Over Time"

def visualize_time_of_visits(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    visits_per_hour = df['Hour'].value_counts().sort_index()
    sns.barplot(x=visits_per_hour.index, y=visits_per_hour.values, ax=ax)
    ax.set_title('Number of Visits by Hour of Day')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Number of Visits')
    return fig, "Number of Visits by Hour of Day"

def visualize_main_interests(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    page_counts = df['Page'].value_counts()
    sns.barplot(x=page_counts.index, y=page_counts.values, ax=ax)
    ax.set_title('Main Interests (Most Visited Pages)')
    ax.set_xlabel('Page')
    ax.set_ylabel('Number of Visits')
    plt.xticks(rotation=45)
    return fig, "Main Interests"

def get_basic_visualizations(df):
    visualizations = []
    visualizations.append(visualize_country_of_origin(df))
    visualizations.append(visualize_number_of_visits(df))
    visualizations.append(visualize_time_of_visits(df))
    visualizations.append(visualize_main_interests(df))
    return visualizations
