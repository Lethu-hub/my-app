import pandas as pd

# Function to read and parse web server log files
def read_parse_log(file_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)
    
    # Split the 'Timestamp' column into separate date and time columns
    split_timestamp = df['Timestamp'].str.split(' ', n=1, expand=True)
    
    # Check if the split was successful
    if len(split_timestamp.columns) == 2:
        df[['Date', 'Time']] = split_timestamp
    else:
        # If split failed, set 'Date' and 'Time' to NaN
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

# Example usage:
input_file = 'synthetic_web_logs.csv'
output_file = 'preprocessed_web_logs.csv'

# Read and parse web server log file
log_data = read_parse_log(input_file)

# Save preprocessed data to CSV
log_data.to_csv(output_file, index=False)
print(f"Preprocessed data saved to {output_file}")
