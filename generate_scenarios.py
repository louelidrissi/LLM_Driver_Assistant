import random
import csv
import pandas as pd
import numpy as np
from itertools import product
from generate_context import add_env_description
from generate_risk import add_risk_score


'''
    Simulate driving scenarios to create training and testing datasets.
    Labels are created following a sample of Driving Monitoring Dataset (DMD) 

'''

state_mapping = {
   "driver_actions" : ["drinking", "radio", "reach_side", "reach_backseat", "safe_drive", "standstill_or_waiting", "texting_right", "texting_left", "hair_and_makeup", "change_gear", "phonecall_right", "phonecall_left", "unclassified"],
   "hands_using_wheel": ["both", "only_left", "only_right", "none"],
   "hand_on_gear": ["hand_on_gear", "hand_not_on_gear"],
   "objects_in_scene": ["bottle","cellphone", "hair_comb", "none"],
   "talking": ["talking","not_talking"],
   "gaze_on_road": ["looking_road", "not_looking_road"],
   "eyes_state": ["close", "closing", "open", "opening", "undefined" ],
   "yawning": ["Yawning with hand",  "Yawning without hand", "not_yawning"],
}

def generate_driver_state(danger_mode):
    ''' Generate description of driver: actions, eye state, gaze, objects appearing in scene, talking or yawning, hands on wheel. '''
    
    actionlist = ["safe_drive", "standstill_or_waiting","reach_side", "reach_backseat", "radio", "change_gear", "hair_and_makeup", "drinking", "texting_right", "texting_left", "phonecall_right", "phonecall_left", "unclassified"]

    count = 0
    # initiate dictionary 
    driver_state = {
        "driver_actions": "NA",
        "objects_in_scene" : "NA",
        "hand_on_gear": "NA",
        "hands_using_wheel": "NA",
        "talking": "NA",
        "gaze_on_road": "NA",
        "eyes_state": "NA",
        "yawning": "NA",
    }
    driver_state_list = []
    for action in actionlist:

        if action == "safe_drive":

            hands_using_wheel_options = ["both","hand_on_gear"]#random.choice()
            eyes_state_options =["open", "opening"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": "NA",
                "talking": "not_talking",
                "gaze_on_road": "looking_road",
                "eyes_state": "open",
                "yawning": "not_yawning",
            }
            for hands_using_wheel, eyes_state in product(hands_using_wheel_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["eyes_state"] = eyes_state
                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "standstill_or_waiting":
            hands_using_wheel_options = ["both", "none", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking", "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
               "driver_actions": action,
               "objects_in_scene" : "none",
               "hand_on_gear": "NA",
               "hands_using_wheel": random.choice(["both", "only_left", "only_right","hand_on_gear"]),
               "talking": random.choice(["talking", "not_talking", "Yawning"]),
               "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
               "eyes_state": random.choice(state_mapping["eyes_state"]),
               "yawning": "NA",
           }
            for hands_using_wheel, talking, gaze_on_road, eyes_state in product(hands_using_wheel_options, talking_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state
                #print(driver_state)
                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "reach_side":
            hands_using_wheel_options = ["none","only_left", "only_right"]
            talking_options = ["talking", "not_talking", "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": random.choice(["only_left", "only_right"]),
                "talking": random.choice(["talking", "not_talking", "Yawning without hand"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "NA",
            }
            for hands_using_wheel, talking, gaze_on_road, eyes_state in product(hands_using_wheel_options, talking_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "reach_backseat":
            hands_using_wheel_options = [ "none", "only_left", "only_right"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": [ "only_left", "only_right"],
                "talking": random.choice(["talking", "not_talking", "Yawning"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "NA",
            }
            for talking, gaze_on_road, hands_using_wheel, eyes_state in product(talking_options, gaze_on_road_options, hands_using_wheel_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "radio":
            hands_using_wheel_options = ["none", "only_left"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": ["only_left", "only_right"],
                "talking":  random.choice(["talking","not_talking","Yawning"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "NA",
            }
            for talking, gaze_on_road, eyes_state, hands_using_wheel in product(talking_options, gaze_on_road_options, eyes_state_options, hands_using_wheel_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "change_gear":
            hands_using_wheel_options = ["none", "only_left","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "hand_on_gear",
                "hands_using_wheel": "only_left",
                "talking": random.choice(["talking","not_talking","Yawning"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": random.choice(state_mapping["eyes_state"]),
                "yawning": "NA",
            }
            for talking, gaze_on_road, eyes_state, hands_using_wheel in product(talking_options, gaze_on_road_options, eyes_state_options, hands_using_wheel_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "hair_and_makeup":
            hands_using_wheel_options = ["only_left", "only_right"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
               "driver_actions": action,
               "objects_in_scene" : "hair_comb",
               "hand_on_gear": "NA",
               "hands_using_wheel": random.choice(["only_left", "only_right"]),
               "talking": random.choice(["talking","not_talking","Yawning"]),
               "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
               "eyes_state": "open",
               "yawning": "NA",
            }
            for hands_using_wheel, talking, gaze_on_road, eyes_state in product(hands_using_wheel_options, talking_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)


        if action == "drinking":
            hands_using_wheel_options = ["none","only_left", "only_right"]
            #talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "bottle",
                "hand_on_gear": "NA",
                "hands_using_wheel": random.choice(["only_left", "only_right"]),
                "talking": "NA",
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": random.choice(state_mapping["eyes_state"]),
                "yawning": "NA",
            }
            for hands_using_wheel, gaze_on_road, eyes_state in product(hands_using_wheel_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                #driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "texting_right":
            hands_using_wheel_options = ["none", "only_left","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "phone",
                "hand_on_gear": "NA",
                "hands_using_wheel": "only_left",
                "talking": random.choice(["talking","not_talking","Yawning"]),
                "gaze_on_road": "not_looking_road",
                "eyes_state": "open",
                "yawning": "NA",
            }
            for talking, hands_using_wheel_options, gaze_on_road, eyes_state in product(talking_options, hands_using_wheel_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "texting_left":
            hands_using_wheel_options = ["none", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "phone",
                "hand_on_gear": "NA",
                "hands_using_wheel":  "only_right",
                "talking": random.choice(["talking","not_talking","Yawning without hand"]),
                "gaze_on_road": "not_looking_road",
                "eyes_state": "open",
                "yawning":  "NA",
            }
            for talking, hands_using_wheel, gaze_on_road, eyes_state in product(talking_options, hands_using_wheel_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "phonecall_right":
            hands_using_wheel_options = ["none", "only_left" ,"hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "phone",
                "hand_on_gear": "NA",
                "hands_using_wheel": "only_left",
                "talking": "talking",
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "not_yawning",
            }
            for gaze_on_road, hands_using_wheel, talking, eyes_state in product(gaze_on_road_options, hands_using_wheel_options, talking_options, eyes_state_options) :
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "phonecall_left":
            hands_using_wheel_options = [ "none", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "phone",
                "hand_on_gear": "NA",
                "hands_using_wheel": "only_right",
                "talking": "talking",
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "not_yawning",
            }
            for gaze_on_road, hands_using_wheel, talking, eyes_state in product(gaze_on_road_options, hands_using_wheel_options, talking_options, eyes_state_options) :
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)

        if action == "unclassified":
            hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": random.choice(["both", "only_left", "only_right","hand_on_gear"]),
                "talking": random.choice(["talking", "not_talking", "Yawning"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": random.choice(state_mapping["eyes_state"]),
                "yawning": "NA",
            }
            for hands_using_wheel, talking, gaze_on_road, eyes_state in product(hands_using_wheel_options, talking_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()

                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state

                for _ in range(100):
                    driver_state = add_env_description(action, driver_state, danger_mode)
                    driver_state = add_risk_score(driver_state)
                    driver_state_list.append(driver_state)
    
    #print(count)
    return driver_state_list

def save_to_csv(data, output_file):
    df = pd.DataFrame(data)

    #if "risk_score" in df.columns:
    #    df["risk_score"] = df["risk_score"].round(5)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].round(3)

    df_unique = df.drop_duplicates()

    print(f"Original rows: {len(df)}, Unique rows: {len(df_unique)}")


    df_unique.to_csv(output_file, index=False)

    #df.to_csv(output_file, index=False)
    #print("Number of rows:", df.shape[0])
    #print("Number of columns:", df.shape[1])

def main():
  
    # Generate training dataset, danger_mode = True
    driver_state_list = generate_driver_state(True)
    save_to_csv(driver_state_list, "training_scenarios.csv")

    # Generate testing dataset, danger_mode = False
    driver_state_list = generate_driver_state(False)
    save_to_csv(driver_state_list, "testing_scenarios.csv")
   

if __name__ == "__main__":
    main()

