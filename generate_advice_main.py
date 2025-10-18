import csv
import random
import json 
import pandas as pd

from generate_state_classification import classify_behavior
from preprocess_advice import get_coherent_input
from generate_scenario_advice import get_advice



''' Creates training and testing datasets with situation and corresponding advice.
    Each advice has up to 2 mitigation steps according to risk priority'''


def get_input_advice(scenarios_list):
    ''' Advice based on priority risk. 
        De-escalate risk for each scenario. '''
    results = []
    filtered_list = []
    #general_input = "The driver is {driver_actions}, {gaze_on_road}, and using {hands_using_wheel} hand(s) on the wheel. Driver is {talking} and/or {yawning} and his eyes {eyes_state}.Weather is {weather}, traffic is {traffic_density}, and the car is {car_speed} speed limit on a {road_type} road. Behavior classification detected: {classification}."
    for scenario in scenarios_list:
        #print(scenario)
        #clean_scenario = clean_input(scenario)
        # Create input text describing scenario
        coherent_input, input_as_dict = get_coherent_input(scenario)
        # Generate advice for input  
        advice_text = get_advice(scenario)
        #print("advice_text", advice_text)
        # Limit advice to maximum 2 per scenario
        advice = advice_text[:3]
        advice_text = " ".join(advice)
        results.append({"input": coherent_input, "advice": advice_text})
        filtered_list.append({"input":input_as_dict, "advice": advice_text})
    return results, filtered_list


def get_results(input_filename, output_filename):
    # Classify all scenarios
    classified_scenarios_list  = classify_behavior(input_filename, output_filename)
    # Generate input with corresponding advice, then shuffle
    results, filtered_list = get_input_advice(classified_scenarios_list)
    random.shuffle(results)
    return results, filtered_list

def save_as_jsonl(instruction, data, output_filepath):
    with open(output_filepath, "w", encoding="utf-8") as f_out:
        for record in data:
            json_record = {
                "instruction": instruction,
                "input": record["input"],
                "output": record["advice"]
            }
            f_out.write(json.dumps(json_record) + "\n")
    print("saved as json l", output_filepath)

def save_as_csv(data, output_filepath):
    # does not include instruction
    with open(output_filepath, "w", newline='', encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=["input", "advice"])
        writer.writeheader()
        for record in data:
            writer.writerow(record)
    print("saved as csv", output_filepath)


def main():

    instruction = "Give driving advice based on the situation."

    # Training Data Classified and Unique Filenames
    csv_training_filename = "training_dataset_corrected.csv"
    csv_training_classified_filename = "training_dataset_corrected_classified.csv"

    training_results, filtered_training = get_results(csv_training_filename, csv_training_classified_filename)
    df_filtered_training = pd.DataFrame(filtered_training)
    
    df_filtered_training.to_csv('filtered_training.csv', index=False)

    # Training Advice Filenames 
    training_advice_csv_filename = "training_input_advice.csv"
    training_advice_jsonl_filename = "training_input_advice.jsonl"

    save_as_csv(training_results, training_advice_csv_filename)
    save_as_jsonl(instruction, training_results, training_advice_jsonl_filename)


    # Testing Data Classified and Unique Filenames
    csv_testing_filename = "testing_dataset_corrected.csv"
    csv_testing_classified_filename  = "training_dataset_corrected_classified.csv"

    testing_results, filtered_testing = get_results(csv_testing_filename, csv_testing_classified_filename)

    df = pd.DataFrame(filtered_testing)
    df.to_csv('filtered_testing.csv', index=False)

    # Testing Advice Filenames
    testing_advice_csv_filename = "testing_input_advice.csv"
    testing_advice_jsonl_filename = "testing_input_advice.jsonl"

    save_as_csv(testing_results, testing_advice_csv_filename)
    save_as_jsonl(instruction, testing_results, testing_advice_jsonl_filename)

    print(f"New training set size: {len(training_results)}")
    print(f"New testing set size: {len(testing_results)}")

    #New training set size: 10168
    #New testing set size: 9923

if __name__ == "__main__":
    main()


