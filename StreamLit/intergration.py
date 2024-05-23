import os
import pandas as pd

def integrate_csv_files(input_directory, output_file):
    # Initialize an empty list to hold the data from all files
    all_logs = []

    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]

    # Counter to track progress
    log_count = 0
    file_count = 0
    total_files = len(csv_files)

    try:
        # Read each CSV file and append its content to the list
        for csv_file in csv_files:
            file_path = os.path.join(input_directory, csv_file)
            log_df = pd.read_csv(file_path)
            all_logs.append(log_df)

            # Update log count and file count
            log_count += len(log_df)
            file_count += 1

            # Provide feedback every 500 logs
            if log_count % 500 == 0:
                print(f"Processed {log_count} logs so far...")

            # Provide feedback for every file
            print(f"Processed file {file_count}/{total_files}")

        # Concatenate all DataFrames
        all_logs_df = pd.concat(all_logs, ignore_index=True)

        # Save the combined DataFrame to a single CSV file
        all_logs_df.to_csv(output_file, index=False)
        print(f"Integration successful. Integrated web logs saved to {output_file}")

    except Exception as e:
        print(f"Integration failed: {e}")

# Directory containing the individual log files
input_directory = 'weblogs'

# Output file path
output_file = 'synthetic_web_logs.csv'

# Integrate the CSV files
integrate_csv_files(input_directory, output_file)
