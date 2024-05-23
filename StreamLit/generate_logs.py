import random
import pandas as pd
from datetime import datetime, timedelta

# Function to generate synthetic test data of web server logs
def generate_web_logs(start_date, end_date, num_logs):
    # List of sports
    sports = ['football', 'basketball', 'swimming', 'cycling', 'tennis', 'volleyball', 'gymnastics', 'boxing', 'surfing', 'athletics']
    
    # Generate random web server logs
    logs = []
    current_date = start_date
    for _ in range(num_logs):
        timestamp = current_date.strftime('%Y-%m-%d %H:%M:%S')
        ip_address = f'{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}'
        request_method = random.choice(['GET', 'POST'])
        endpoint = f'/{random.choice(sports)}.html'
        status_code = random.choice([200, 404, 500])
        logs.append([timestamp, ip_address, request_method, endpoint, status_code])
        current_date += timedelta(minutes=random.randint(1, 60))  # Increment timestamp randomly
    
    # Create DataFrame
    df = pd.DataFrame(logs, columns=['Timestamp', 'IP Address', 'Request Method', 'Endpoint', 'Status Code'])
    
    return df

# Example usage:
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 2)
num_logs = 1000  # Adjust as needed
web_logs = generate_web_logs(start_date, end_date, num_logs)

# Save to CSV
web_logs.to_csv('synthetic_web_logs.csv', index=False)
print("Web logs saved to synthetic_web_logs.csv")
