import os
import pandas as pd

def integrate_csv_files(input_directory, output_file):
    # Get list of CSV files in the input directory
    csv_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]
    
    # Initialize an empty list to store DataFrame objects
    dataframes = []
    
    # Iterate over each CSV file and read its data into a DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(input_directory, csv_file)
        data = pd.read_csv(file_path)
        dataframes.append(data)
    
    # Concatenate all DataFrame objects in the list along the rows
    integrated_data = pd.concat(dataframes, ignore_index=True)
    
    # Save the integrated data to a new CSV file
    integrated_data.to_csv(output_file, index=False)
    print(f"Integration successful. Integrated data saved to {output_file}")

# Example usage:
input_directory = 'StreamLit/weblogs'
output_file = 'StreamLit/synthetic_web_logs.csv'
integrate_csv_files(input_directory, output_file)
