import random
import pandas as pd
from datetime import datetime, timedelta
import os

# Function to generate synthetic test data for web server logs
def generate_web_logs(num_logs):
    # Lists for status codes and sports/pages
    status_codes = [20 + i for i in range(1000)]
    sports = [f'sport_{i}' for i in range(1000)]
    pages = sports + ['home']

    # Country-specific IP address ranges (simplified examples)
    ip_ranges = {
        'USA': (3, 34),       # AWS IP ranges for USA
        'Germany': (13, 14),  # AWS IP ranges for Germany
        'Japan': (13, 52),    # AWS IP ranges for Japan
        'India': (13, 14),    # AWS IP ranges for India
        'Australia': (13, 52) # AWS IP ranges for Australia
    }
    countries = list(ip_ranges.keys())

    # Generate random web server logs
    logs = []
    for _ in range(num_logs):
        timestamp = (datetime.now() - timedelta(minutes=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S')
        country = random.choice(countries)
        ip_range = ip_ranges[country]
        ip_address = f'{random.randint(ip_range[0], ip_range[1])}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        request_method = random.choice(['GET', 'POST'])
        endpoint = f'/{random.choice(pages)}.html'
        status_code = random.choice(status_codes)
        logs.append([timestamp, ip_address, request_method, endpoint, status_code, country])
    
    # Create DataFrame
    df = pd.DataFrame(logs, columns=['Timestamp', 'IP Address', 'Request Method', 'Endpoint', 'Status Code', 'Country'])
    
    return df

# Function to save log to a CSV file
def save_log_to_csv(df, directory):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    filename = f'web_log_{timestamp}.csv'
    file_path = os.path.join(directory, filename)

    # Debugging output
    print(f"Attempting to save log to {file_path}...")
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist. Attempting to create it.")
        os.makedirs(directory, exist_ok=True)
    df.to_csv(file_path, index=False)
    if os.path.exists(file_path):
        print(f"Web log successfully saved to {file_path}")
    else:
        print(f"Failed to save web log to {file_path}")

# Directory where log files will be saved
output_directory = 'weblogs'

# Number of logs per file
logs_per_file = 1000

# Generate and save log files
num_files = 10  # Adjust this to change the number of files generated each run
for i in range(num_files):
    log_data = generate_web_logs(logs_per_file)
    save_log_to_csv(log_data, output_directory)
    print(f"Generated and saved file {i+1}/{num_files}")
