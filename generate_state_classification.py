import csv

state_classification = {
    "driver_actions": {
        "reach_side": "distraction",
        "reach_backseat": "high_distraction",
        "radio": "distraction",
        "hair_and_makeup": "high_distraction",
        "drinking": "distraction",
        "texting_right": "high_distraction",
        "texting_left": "high_distraction",
        "phonecall_right": "distraction",
        "phonecall_left": "distraction",  
    },
    "hands_using_wheel": {
        "none": "high_distraction"
    },
    "talking": {
        "talking": "distraction",
    },
    "gaze_on_road": {
        "not_looking_road": "high_distraction"
    },
    "eyes_state": {
        "closing": "drowsiness",
        "close": "drowsiness"
    },
    "yawning": {
        "Yawning without hand": "drowsiness",
        "Yawning with hand": "drowsiness",
        "Yawning": "drowsiness",
        "yawning": "drowsiness"
    }
}

allowed_classes = {
    "distraction,drowsiness,high_distraction",
    "drowsiness,high_distraction",
    "distraction,high_distraction",
    "distraction,drowsiness",
    "high_distraction",
    "distraction",
    "drowsiness"
}

def classify_behavior(csv_filename, output_file):
    scenarios_list = []
    with open(csv_filename, "r", encoding="utf-8", newline="") as f_in, \
         open(output_file, "w", encoding="utf-8", newline="") as f_out:

        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + ["classification"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            classifications = set()  # use a set to avoid duplicates

            # Check each column in the row against your classification mappings
            for col, mapping in state_classification.items():
                if col in row and row[col] in mapping:
                    classifications.add(mapping[row[col]])
                    #print("classifications", classifications)
            # Handle case if no condition matched
            if not classifications:
                classifications.add("un")

            # Convert the set to a comma-separated string for CSV output
            classification_str = ",".join(sorted(classifications))
            if classification_str not in allowed_classes and classification_str != "safe":
                classification_str = "un"

            row["classification"] = classification_str    
            #print("classifications", classification_str)
            scenarios_list.append(row)
            writer.writerow(row)
    print("saved as csv classified", output_file)
    return scenarios_list