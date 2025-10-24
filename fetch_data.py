import os
from collections import defaultdict
import csv

'''
Used to check for file names repetition under different labels 
'''

base_path = "/Users/louelidrissi/LLM/data/all_trial_2"
file_labels = {}

count = 0
for num_folder in os.listdir(base_path):
    if num_folder == ".DS_Store":
            continue

    #print(label_folder)
    num_path = os.path.join(base_path, num_folder)
    if not os.path.isdir(num_path) or not num_folder.isdigit():
        continue  # Skip if not a main label folder (0–9)

    # Go two levels deep inside
    for label_folder in os.listdir(num_path):
        if label_folder == ".DS_Store":
            continue

        label_path = os.path.join(num_path, label_folder)
        if not os.path.isdir(label_path):
            continue
        #print("label_folder", label_folder)

        for subfolder in os.listdir(label_path):
            #print(" subfolder", subfolder)
            if subfolder == ".DS_Store":
                continue
            # driver state folder path
            
                       # find .avi files
            #for file_name in os.listdir(sub_path):
              #  if not file_name.lower().endswith(".avi"):
              #      continue
            #print("label_folder", label_folder)
           # print("subfolder", subfolder)
            # store file under its label name
            if subfolder in file_labels:
               # print(subfolder, label_folder)
                file_labels[subfolder].append(label_folder)
            else:
                #print("2",subfolder, label_folder)
                file_labels[subfolder] = [label_folder]
    count = count+1
    if count == 3:
        break
                
print(file_labels)

# Print files that appear in multiple label folders
'''
# Open a CSV file to write
with open("file_labels.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header
    writer.writerow(["filename", "labels"])
    
    # Write each file and its labels
    for file, labels in file_labels.items():
        writer.writerow([file, ", ".join(labels)])

'''


