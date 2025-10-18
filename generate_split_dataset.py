import json
import csv
import random
import pandas as pd

from sklearn.model_selection import train_test_split


def split_dataset(training_filename, testing_filename):
    # Split data into risky and non-risky
    risky_data = pd.read_csv(training_filename)
    non_risky_data = pd.read_csv(testing_filename)

    R = len(risky_data)
    N = len(non_risky_data)

    # Calculate how many non-risky samples to keep in training
    N_train = int((N - 0.20 * R) / 1.2)
    N_test = N - N_train

    # Shuffle non-risky data before split
    non_risky_data = non_risky_data.sample(frac=1, random_state=42).reset_index(drop=True)

    # Split non-risky data accordingly
    non_risky_train = non_risky_data.iloc[:N_train]
    non_risky_test = non_risky_data.iloc[N_train:]

    # Combine risky + non-risky train for final training set
    final_train = pd.concat([risky_data, non_risky_train])
    final_test = non_risky_test

    print(f"Training size (risky + non-risky train): {len(final_train)}")
    print(f"Testing size: {len(final_test)}")
    print(f"Test set is approx. {len(final_test)/len(final_train)*100:.2f}% of training set size")
    return final_train, final_test

def save_to_csv(training_data, testing_data):
    # Save datasets
    training_data.to_csv('training_input_advice_80.csv', index=False)
    testing_data.to_csv('testing_input_advice_20.csv', index=False)

    
    return

def save_as_jsonl(data, output_filepath):
    instruction = "Give driving advice based on the situation."
    with open(output_filepath, "w", encoding="utf-8") as f_out:
        for record in data:
            json_record = {
                "instruction": instruction,
                "input": record["input"],
                "output": record["advice"]
            }
            f_out.write(json.dumps(json_record) + "\n")
    print("saved as json l", output_filepath)

def main():
    # Advice filenames 
    training_filename = "training_input_advice.csv"
    testing_filename = "testing_input_advice.csv"

    # Split data such as testing data rows are 20% of training data rows
    final_train, final_test = split_dataset(training_filename, testing_filename)
    # Check that rows in training and testing data are duplicate-free and mutually exclusive
    #final_train_unique, final_test_unique = check_for_duplicates(final_train, final_test)
    # Save results
    training_json_filename = 'training_input_advice_80.jsonl'
    testing_json_filename = 'testing_input_advice_20.jsonl'
    save_to_csv(final_train, final_test)

    final_train['instruction'] = "Give driving advice based on the situation."
    final_test['instruction'] = "Give driving advice based on the situation."
   # save_as_jsonl(final_train, training_json_filename)
    #save_as_jsonl(final_test, testing_json_filename )

    print(f"New training set size: {len(final_train)}")
    print(f"New testing set size: {len(final_test)}")
    
    final_train.to_json('training_input_advice_80.jsonl', orient='records', lines=True)
    final_test.to_json('testing_input_advice_20.jsonl', orient='records', lines=True)

if __name__ == "__main__":
    main()

