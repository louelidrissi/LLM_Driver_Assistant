import random
import csv
import pandas as pd
from itertools import product

state_mapping = {
   "driver_actions" : ["drinking", "radio", "reach_side", "reach_backseat", "safe_drive", "standstill_or_waiting", "standstill_or_waiting", "texting_right", "texting_left", "hair_and_makeup", "change_gear", "phonecall_right", "phonecall_left", "unclassified"],
   "hands_using_wheel": ["both", "only_left", "only_right", "none"],
   "hand_on_gear": ["hand_on_gear", "hand_not_on_gear"],
   "objects_in_scene": ["bottle","cellphone", "hair_comb", "none"],
   "talking": ["talking","not_talking"],
   "gaze_on_road": ["looking_road", "not_looking_road"],
   "eyes_state": ["close", "closing", "open", "opening", "undefined" ],
   "yawning": ["Yawning with hand",  "Yawning without hand", "not_yawning"],
}

driver_behavior_frequencies = {
    "driver_actions": "NA",
    "objects_in_scene" : "NA",
    "hand_on_gear": "NA",
    "hands_using_wheel": "NA",
    "talking": "NA",
    "gaze_on_road": "NA",
    "eyes_state": "NA",
    "yawning": "NA",
}


actionlist = ["safe_drive", "standstill_or_waiting","reach_side", "reach_backseat", "radio", "change_gear", "hair_and_makeup", "drinking", "texting_right", "texting_left", "phonecall_right", "phonecall_left", "unclassified"]

def driver_state_test():
    # initiate dictionary 
    count = 0

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
            for hands_using_wheel in hands_using_wheel_options:
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                
                driver_state_list.append(driver_state)

        if action == "standstill_or_waiting":
            hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
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
                print(driver_state)
                driver_state_list.append(driver_state)

        if action == "reach_side":
            hands_using_wheel_options = ["only_left", "only_right"]
            talking_options = ["talking", "not_talking", "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

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
            for hands_using_wheel, talking, gaze_on_road in product(hands_using_wheel_options, talking_options, gaze_on_road_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "reach_backseat":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": "only_left",
                "talking": random.choice(["talking", "not_talking", "Yawning without hand"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "NA",
            }
            for talking, gaze_on_road in product(talking_options, gaze_on_road_options):
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "radio":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "NA",
                "hands_using_wheel": "only_left",
                "talking":  random.choice(["talking","not_talking","Yawning without hand"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": "open",
                "yawning": "NA",
            }
            for talking, gaze_on_road in product(talking_options, gaze_on_road_options):
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "change_gear":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "none",
                "hand_on_gear": "hand_on_gear",
                "hands_using_wheel": "only_left",
                "talking": random.choice(["talking","not_talking","Yawning without hand"]),
                "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
                "eyes_state": random.choice(state_mapping["eyes_state"]),
                "yawning": "NA",
            }
            for talking, gaze_on_road, eyes_state in product(talking_options, gaze_on_road_options, eyes_state_options):
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "hair_and_makeup":
            hands_using_wheel_options = ["only_left", "only_right"]
            talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
               "driver_actions": action,
               "objects_in_scene" : "hair_comb",
               "hand_on_gear": "NA",
               "hands_using_wheel": random.choice(["only_left", "only_right"]),
               "talking": random.choice(["talking","not_talking","Yawning without hand"]),
               "gaze_on_road": random.choice(state_mapping["gaze_on_road"]),
               "eyes_state": "open",
               "yawning": "NA",
            }
            for hands_using_wheel, talking, gaze_on_road in product(hands_using_wheel_options, talking_options, gaze_on_road_options):
                count = count+1
                driver_state = driver_state.copy()
                driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)


        if action == "drinking":
            hands_using_wheel_options = ["only_left", "only_right"]
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
                driver_state_list.append(driver_state)

        if action == "texting_right":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning without hand"]
            #gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

            driver_state = {
                "driver_actions": action,
                "objects_in_scene" : "phone",
                "hand_on_gear": "NA",
                "hands_using_wheel": "only_left",
                "talking": random.choice(["talking","not_talking","Yawning without hand"]),
                "gaze_on_road": "not_looking_road",
                "eyes_state": "open",
                "yawning": "NA",
            }
            for talking in talking_options:
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                #driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "texting_left":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            talking_options = ["talking", "not_talking",  "Yawning without hand"]
            #gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

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
            for talking in talking_options:
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                driver_state["talking"] = talking
                #driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "phonecall_right":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            #talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

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
            for gaze_on_road in gaze_on_road_options:
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                #driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
                driver_state_list.append(driver_state)

        if action == "phonecall_left":
            #hands_using_wheel_options = ["both", "only_left", "only_right","hand_on_gear"]
            #talking_options = ["talking", "not_talking",  "Yawning without hand"]
            gaze_on_road_options = state_mapping["gaze_on_road"]
            #eyes_state_options = state_mapping["eyes_state"]

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
            for gaze_on_road in gaze_on_road_options:
                count = count+1
                driver_state = driver_state.copy()
                #driver_state["hands_using_wheel"] = hands_using_wheel
                #driver_state["talking"] = talking
                driver_state["gaze_on_road"] = gaze_on_road
                #driver_state["eyes_state"] = eyes_state
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
                driver_state_list.append(driver_state)

    print(count)
    return driver_state_list

driver_state_list = driver_state_test()


def select_behavior_frequency():
    # phone for x amount, x yawns per period of time, etc ...
    # look up see frequency of behavior 


    return



def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("driver_states_all_combos.csv", index=False)
    print(" CSV saved!")

save_to_csv(driver_state_list)
