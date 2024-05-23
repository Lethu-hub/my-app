import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geoip2.database
import time

# Function to read and parse web server log files
def read_parse_log(file_path):
    start_time = time.time()
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['Hour'] = df['Timestamp'].dt.hour
    end_time = time.time()
    print(f"read_parse_log executed in {end_time - start_time:.2f} seconds")
    return df

# Function to get country from IP address
def get_country_from_ip(ip, reader):
    try:
        response = reader.country(ip)
        return response.country.name
    except:
        return 'Unknown'

# Function to analyze web server logs
def analyze_logs(log_data, geoip_db_path):
    start_time = time.time()
    reader = geoip2.database.Reader(geoip_db_path)
    log_data['Country'] = log_data['IP Address'].apply(lambda ip: get_country_from_ip(ip, reader))
    visits_by_country = log_data['Country'].value_counts()
    visits_over_time = log_data['Hour'].value_counts().sort_index()
    main_interests = log_data['Endpoint'].apply(lambda x: x.split('/')[1].replace('.html', '')).value_counts()
    main_interests_by_country = log_data.groupby('Country')['Endpoint'].apply(
        lambda x: x.apply(lambda y: y.split('/')[1].replace('.html', '')).value_counts().head(1)).reset_index()
    end_time = time.time()
    print(f"analyze_logs executed in {end_time - start_time:.2f} seconds")
    return {
        'visits_by_country': visits_by_country,
        'visits_over_time': visits_over_time,
        'main_interests': main_interests,
        'main_interests_by_country': main_interests_by_country
    }

# Function to create visualizations
def create_visualizations(analysis_results):
    start_time = time.time()
    visualizations = []

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=analysis_results['visits_by_country'].index, y=analysis_results['visits_by_country'].values, ax=ax1)
    ax1.set_title('Number of Visits by Country')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Number of Visits')
    plt.xticks(rotation=90)
    visualizations.append((fig1, 'Number of Visits by Country'))
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=analysis_results['visits_over_time'].index, y=analysis_results['visits_over_time'].values, ax=ax2)
    ax2.set_title('Number of Visits Over Time')
    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Number of Visits')
    visualizations.append((fig2, 'Number of Visits Over Time'))
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=analysis_results['main_interests'].index, y=analysis_results['main_interests'].values, ax=ax3)
    ax3.set_title('Main Interests Based on Viewed Sports')
    ax3.set_xlabel('Sport')
    ax3.set_ylabel('Number of Views')
    plt.xticks(rotation=90)
    visualizations.append((fig3, 'Main Interests Based on Viewed Sports'))
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=analysis_results['main_interests_by_country']['Country'], 
                y=analysis_results['main_interests_by_country']['Endpoint'], ax=ax4)
    ax4.set_title('Main Interests by Country')
    ax4.set_xlabel('Country')
    ax4.set_ylabel('Main Interest')
    plt.xticks(rotation=90)
    visualizations.append((fig4, 'Main Interests by Country'))
    
    end_time = time.time()
    print(f"create_visualizations executed in {end_time - start_time:.2f} seconds")
    return visualizations

if __name__ == "__main__":
    log_file_path = 'StreamLit/synthetic_web_logs.csv'
    geoip_db_path = 'StreamLit/GeoLite2-Country.mmdb'
    log_data = read_parse_log(log_file_path)
    analysis_results = analyze_logs(log_data, geoip_db_path)
    visualizations = create_visualizations(analysis_results)
    for fig, _ in visualizations:
        plt.figure(fig.number)
        plt.show()
