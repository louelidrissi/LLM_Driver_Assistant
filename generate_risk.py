


'''
    Focus is on detecting drowsiness and distraction
    Environment context & speed are equally contributing factors

'''


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


env_mapping = {
    "road_type": ["highway", "urban", "rural"],
    "weather": ["clear", "rain", "fog", "snow"],
    "time_of_day": ["morning", "afternoon", "evening", "night"],
    "traffic_density": ["low", "medium", "high"],
    "car_speed": ["none", "under", "over", "severe_over"]
}


# state risk is influenced by duration/frequency 
state_risk = {
    "driver_actions": {
        "safe_drive": 0.0,
        "standstill_or_waiting": 0.0,
        "reach_side": 0.4,
        "reach_backseat": 0.6,
        "radio": 0.25,
        "change_gear": 0.0,
        "hair_and_makeup": 0.6,
        "drinking": 0.2,
        "texting_right": 0.8,
        "texting_left": 0.8,
        "phonecall_right": 0.4,
        "phonecall_left": 0.4,
        "unclassified": 1
    },
    "hands_using_wheel": {
        "both": 0,
        "only_left": 0.1, # accounted for in actions, not sure how many scenarios only have it 
        "only_right": 0.1,      # TO CHECK 
        "none": 1.0
    },
    "hand_on_gear": {
        "hand_on_gear": 0.0,
        "hand_not_on_gear": 0.0 # matters, but sometimes not needed, especially if car is automatic
    },
    "objects_in_scene": {
                        
        "none": 0.0,  # will change if add scenarios where they only appear without the task
        "bottle": 0.1, # TO CHECK 
        "cellphone": 0.1,
        "hair_comb": 0.1
    },
    "talking": {
        "not_talking": 0.0,
        "talking": 0.2
    },
    "gaze_on_road": {
        "looking_road": 0.0,
        "not_looking_road": 0.6
    },
    "eyes_state": {
        "open": 0.0,
        "opening": 0.2,
        "closing": 0.4,
        "close": 0.4,
        "undefined": 0.2
    },
    "yawning": {
        "not_yawning": 0,
        "Yawning without hand": 0.5,
        "Yawning with hand": 0.5,
        "Yawning": 0.5
    }
}

env_risk_map = {
    "road_type": {
        "highway": 0.8,   # long stretches, higher consequences if distracted
        "urban": 0.5,     # more stop-and-go, slightly safer to recover
        "rural": 0.3      # generally lower speed, less traffic
    },
    "weather": {
        "clear": 0.0,
        "rain": 0.5,      # requires more attention
        "fog": 0.75,      # limits visibility, increases risk of distraction
        "snow": 1.0       # extreme risk for inattentive driver
    },
    "time_of_day": {
        "morning": 0.25,  # alertness usually higher
        "afternoon": 0.5, 
        "evening": 0.75,  # circadian dip, more prone to drowsiness
        "night": 1.0      # highest risk of drowsiness
    },
    "traffic_density": {
        "low": 0.3,       # driver may become bored/distracted
        "medium": 0.5,
        "high": 0.8       # complex environment, mistakes more likely
    },
    "car_speed" : {
        "none": 0.0,          # within speed limits
        "under": 0.3,          # slightly under limit, mild risk
        "over": 0.6,           # over limit, moderate risk
        "severe_over": 1.0     # over limit + bad conditions, high risk
    }
}

def get_driver_state_risk(driver_state):
    # Get driver state/behavior risk score
    action_risk = state_risk["driver_actions"].get(driver_state.get("driver_actions", "unclassified"), 0)
    hands_risk = state_risk["hands_using_wheel"].get(driver_state.get("hands_using_wheel", "both"), 0)
    gear_risk = state_risk["hand_on_gear"].get(driver_state.get("hand_on_gear", "hand_on_gear"), 0)
    object_risk = state_risk["objects_in_scene"].get(driver_state.get("objects_in_scene", "none"), 0)
    talking_risk = state_risk["talking"].get(driver_state.get("talking", "not_talking"), 0)
    gaze_risk = state_risk["gaze_on_road"].get(driver_state.get("gaze_on_road", "looking_road"), 0)
    eyes_risk = state_risk["eyes_state"].get(driver_state.get("eyes_state", "undefined"), 0)
    yawning_risk = state_risk["yawning"].get(driver_state.get("yawning", "not_yawning"), 0)

    driver_state_risk = action_risk + hands_risk + gear_risk + object_risk + talking_risk + gaze_risk + eyes_risk + yawning_risk
    
    return driver_state_risk

def get_env_risk(driver_state):
    # Get context/evironment risk score
    road_risk = env_risk_map["road_type"].get(driver_state.get("road_type", "rural"), 0)
    weather_risk = env_risk_map["weather"].get(driver_state.get("weather", "clear"), 0)
    time_risk = env_risk_map["time_of_day"].get(driver_state.get("time_of_day", "morning"), 0)
    traffic_risk = env_risk_map["traffic_density"].get(driver_state.get("traffic_density", "low"), 0)
    
    env_total_risk = road_risk + weather_risk + time_risk + traffic_risk

    return env_total_risk

def get_max_state_risk():
    max_state_risk = (
        max(state_risk["driver_actions"].values()) +
        max(state_risk["hands_using_wheel"].values()) +
        max(state_risk["hand_on_gear"].values()) +
        max(state_risk["objects_in_scene"].values()) +
        max(state_risk["talking"].values()) +
        max(state_risk["gaze_on_road"].values()) +
        max(state_risk["eyes_state"].values()) +
        max(state_risk["yawning"].values())
    )
    return max_state_risk

def get_max_env_risk():
    max_env_risk = (
        max(env_risk_map["road_type"].values()) +
        max(env_risk_map["weather"].values()) +
        max(env_risk_map["time_of_day"].values()) +
        max(env_risk_map["traffic_density"].values())
    )
    return max_env_risk



def add_risk_score(driver_state):
    '''
    Driver state is the main factor to affect the risk score (weighted 0.5),
    followed by environment and speed (weighted 0.25 each)
    '''

    risk_score = 0.0
    global env_risk_map

    state_risk_score = get_driver_state_risk(driver_state)
    max_state_risk = get_max_state_risk()

    #print("env_risk",env_risk_map)

    env_risk_score = get_env_risk(driver_state)
    max_env_risk_score = get_max_env_risk()
    
    #print("max_env_risk_score", max_env_risk_score)
    # Get speed score
    speed_type = driver_state.get("car_speed", "none")  
    speed_risk_score = env_risk_map["car_speed"].get(speed_type, 0)

    max_speed_risk = max(env_risk_map["car_speed"].values())


    risk_score = 0.5*state_risk_score + 0.25*env_risk_score + 0.25*speed_risk_score

    #risk_score = 0.5*state_risk + 0.25*env_risk_score + 0.25*speed_risk
    max_risk_score = (
        0.5 * max_state_risk +
        0.25 * max_env_risk_score +
        0.25 * max_speed_risk
        )

    normalized_risk = risk_score / max_risk_score
    # Keep between 0 and 1
    normalized_risk = min(1.0, max(0.0, normalized_risk))


    # update dictionary 
    driver_state.update({
        "risk_score": normalized_risk 
    })
    
    return driver_state