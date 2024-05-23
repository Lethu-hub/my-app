import random
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_web_logs(num_logs):
    status_codes = [200, 404, 500]
    sports = [f'sport_{i}' for i in range(12)]
    pages = sports + ['home']
    ip_ranges = {
        'USA': (3, 34),
        'Germany': (13, 14),
        'Japan': (13, 52),
        'India': (13, 14),
        'Australia': (13, 52)
    }
    countries = list(ip_ranges.keys())
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
    df = pd.DataFrame(logs, columns=['Timestamp', 'IP Address', 'Request Method', 'Endpoint', 'Status Code', 'Country'])
    return df

def save_log_to_csv(df, directory):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    filename = f'web_log_{timestamp}.csv'
    file_path = os.path.join(directory, filename)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    df.to_csv(file_path, index=False)

def generate_logs():
    output_directory = 'StreamLit/weblogs'
    logs_per_file = 50
    num_files = 10
    for i in range(num_files):
        log_data = generate_web_logs(logs_per_file)
        save_log_to_csv(log_data, output_directory)
