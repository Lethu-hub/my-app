import os
import pandas as pd

def integrate_csv_files(input_directory='StreamLit/weblogs', output_file='StreamLit/synthetic_web_logs.csv'):
    all_logs = []
    csv_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]
    for csv_file in csv_files:
        file_path = os.path.join(input_directory, csv_file)
        log_df = pd.read_csv(file_path)
        all_logs.append(log_df)
    all_logs_df = pd.concat(all_logs, ignore_index=True)
    all_logs_df.to_csv(output_file, index=False)
