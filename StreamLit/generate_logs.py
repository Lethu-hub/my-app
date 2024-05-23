import random
import pandas as pd
from datetime import datetime, timedelta
import os

# Function to generate synthetic test data of web server logs
def generate_web_logs(start_date, end_date, num_logs_per_file, num_files):
    # Create directory if it doesn't exist
    output_directory = 'StreamLit/weblogs'
    os.makedirs(output_directory, exist_ok=True)

    # List of sports
    sports = ['football', 'basketball', 'swimming', 'cycling', 'tennis', 'volleyball', 'gymnastics', 'boxing', 'surfing', 'athletics', 'hockey', 'golf', 'rugby', 'cricket', 'badminton']
    num_sports = len(sports)

    # Error/status codes
    status_codes = [200, 404, 500, 503, 504]
    num_status_codes = len(status_codes)

    # Generate random web server logs for each file
    for file_idx in range(num_files):
        logs = []
        current_date = start_date

        for _ in range(num_logs_per_file):
            timestamp = current_date.strftime('%Y-%m-%d %H:%M:%S')
            ip_address = f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
            request_method = random.choice(['GET', 'POST'])
            endpoint = f'/{random.choice(sports)}.html'
            status_code = random.choice(status_codes)
            logs.append([timestamp, ip_address, request_method, endpoint, status_code])
            current_date += timedelta(minutes=random.randint(1, 60))  # Increment timestamp randomly

        # Create DataFrame
        df = pd.DataFrame(logs, columns=['Timestamp', 'IP Address', 'Request Method', 'Endpoint', 'Status Code'])

        # Save to CSV
        file_name = f'web_logs_{file_idx + 1}.csv'
        file_path = os.path.join(output_directory, file_name)
        df.to_csv(file_path, index=False)
        print(f"Web logs saved to {file_path}")

# Example usage:
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 2)
num_logs_per_file = 100
num_files = 10
generate_web_logs(start_date, end_date, num_logs_per_file, num_files)
