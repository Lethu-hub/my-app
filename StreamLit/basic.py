import pandas as pd

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
