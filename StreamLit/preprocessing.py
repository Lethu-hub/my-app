import pandas as pd

def read_parse_log(file_name):
    df = pd.read_csv(file_name)
    split_timestamp = df['Timestamp'].str.split(' ', n=1, expand=True)
    if len(split_timestamp.columns) == 2:
        df[['Date', 'Time']] = split_timestamp
    else:
        df['Date'] = pd.NaT
        df['Time'] = pd.NaT
    df['Page'] = df['Endpoint'].str.extract(r'\/(\w+)\.html$')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = df['Timestamp'].dt.hour
    return df

def preprocess_logs(input_file='StreamLit/synthetic_web_logs.csv', output_file='StreamLit/preprocessed_web_logs.csv'):
    log_data = read_parse_log(input_file)
    log_data.to_csv(output_file, index=False)
