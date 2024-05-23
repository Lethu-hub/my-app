import os
import pandas as pd

def integrate_csv_files(input_directory='StreamLit/weblogs', output_file='StreamLit/synthetic_web_logs.csv'):
    all_logs = []
    csv_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]
    log_count = 0
    file_count = 0
    total_files = len(csv_files)
    try:
        for csv_file in csv_files:
            file_path = os.path.join(input_directory, csv_file)
            log_df = pd.read_csv(file_path)
            all_logs.append(log_df)
            log_count += len(log_df)
            file_count += 1
            if log_count % 500 == 0:
                print(f"Processed {log_count} logs so far...")
            print(f"Processed file {file_count}/{total_files}")
        all_logs_df = pd.concat(all_logs, ignore_index=True)
        all_logs_df.to_csv(output_file, index=False)
        print(f"Integration successful. Integrated web logs saved to {output_file}")
    except Exception as e:
        print(f"Integration failed: {e}")
