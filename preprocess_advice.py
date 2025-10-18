import csv
import math
from input_template import sentence_templates, fill_template

''' In each scenario,
        emove none and NA and nan values from scenario input text
        & modify input text to get a clear coherent sentence. '''

def get_coherent_input(scenario):
    input_dict = {
        "driver_actions": scenario["driver_actions"],
        "gaze_on_road": scenario["gaze_on_road"],
        "hands_using_wheel": scenario["hands_using_wheel"],
        "talking": scenario["talking"],
        "eyes_state": scenario["eyes_state"],
        "weather": scenario["weather"],
        "traffic_density": scenario["traffic_density"],
        "car_speed": "within_speed_limit" if scenario["car_speed"] == "none" else scenario["car_speed"],
        "road_type": scenario["road_type"],
        "time_of_day": scenario["time_of_day"],
        "classification": scenario["classification"]
    }
    
    updated_dict = {key: fill_template.get(value, value) for key, value in input_dict.items()}
    filtered_updated_dict = {k: v for k, v in updated_dict.items() if v not in ["nan", "NA", "", "un"] and not (isinstance(v, float) and math.isnan(v))}
    
    filtered_templates = []
    for key, template in sentence_templates.items():
        val = updated_dict.get(key, "")
        if val in ["nan", "", "NA", "un"]:
            continue
        filtered_templates.append(template)

    input_text = " ".join(filtered_templates)
    coherent_text = input_text.format(**filtered_updated_dict)


    #print("coherent_text", coherent_text)
    
    return coherent_text, input_dict
    
