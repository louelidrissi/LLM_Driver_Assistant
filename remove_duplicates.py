import random
import csv
import json
import pandas as pd
import numpy as np
import glob



def combine_and_deduplicate_csvs(folder_path, output_path='combined_unique.csv', float_precision=3):
    """
    Combine multiple CSV files, clean minor inconsistencies, 
    and remove duplicate rows (keep only one instance).
    """

    # Find all CSV files in the folder
    csv_files = glob.glob(f"{folder_path}/*.csv")
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return
    print("csv_files", csv_files)

    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        
        # Clean string columns: strip whitespace and lowercase
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
        
        # Round numeric columns to given precision (e.g. risk_score normalized to 1)
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].round(float_precision)
        
        dfs.append(df)

    # Combine all CSVs
    combined_df = pd.concat(dfs, ignore_index=True)

    # Drop duplicates across all CSVs
    unique_df = combined_df.drop_duplicates()

    # Save to new file
    unique_df.to_csv(output_path, index=False)

    print(f"Combined {len(csv_files)} CSV files.")
    print(f"Total rows before cleaning: {len(combined_df)}")
    print(f"Rows after removing duplicates: {len(unique_df)}")
    print(f"Cleaned and unique data saved to: {output_path}")

    return unique_df


def combine_training():
    folder_path = "/Users/louelidrissi/LLM/training_dataset"
    combine_and_deduplicate_csvs(folder_path, output_path='training_scenarios_combined_unique.csv', float_precision=3)

def combine_testing():
    folder_path = "/Users/louelidrissi/LLM/testing_dataset"
    combine_and_deduplicate_csvs(folder_path, output_path='testing_scenarios_combined_unique.csv', float_precision=3)

#combine_training()
combine_testing()