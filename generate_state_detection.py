import random

def detect_drowsiness(scenario):
     # Detect drowsiness second 
    response = random.choice(["Drowsiness detected. Please open the window for air.", "Play some upbeat music, you seem drowsy."])
    return response

def detect_high_distraction(scenario):
     # means not looking at road
    # or make up or texting, backseat 
    # Focus on risky behavior 
    if scenario["hands_using_wheel"] == "none":
        response = "Keep your hands on the wheel, one hand at 8 and one at 4 for better control."
    
    elif scenario["hands_using_wheel"] == "hand_on_gear" and scenario["driver_actions"] in ["texting_left", "texting_right", "phonecall_left", "phonecall_right", "drinking", "hair_and_makeup"]:
        response = random.choice(["Please put your hands on the wheel", " Please keep one hand at 8 and one at 4 for better control."])

    elif scenario["gaze_on_road"] == "not_looking_road":
        response = "Please look ahead, every second matters."
    
    elif scenario["driver_actions"] == "reach_backseat":
        response = "Please pull aside to reach to the backseat."
    
    elif scenario["driver_actions"] in ["texting_left", "texting_right"]:
        response = random.choice(["Please set your phone to Do Not Disturb While Driving mode", "Please use voice assistants to send messages."])
    
    elif scenario["driver_actions"] == "hair_and_makeup":
        response = random.choice(["Please wait until end of the trip for touch ups.", "Please pull aside to get ready."])
    
    return response

def detect_high_speed(scenario):
    if scenario["traffic_density"] == "high":
        response = random.choice(["You are dangerously over speed limit and traffic is dense.", "You are going too fast and traffic is high."])
    
    elif scenario["road_type"] == "highway":
        response = random.choice(["Please slow down, a blink can cost you a long stretch of awareness.", "Please reduce car speed to stay within highway speed limit."])
    
    elif scenario["weather"] in ["snow", "rain"]:
        response = "Please slow down and keep a 6 to 8 seconds following distance due to bad weather."

    elif scenario["time_of_day"] == "night":
        response = "You are dangerously over speed limit. Please make sure you are able to stop whithin range of your headlights." 
    else:
        response = random.choice(["Car speed is dangerously over speed limit", "Please slow down and stay within speed limits."])

    return response

def detect_speed(scenario):
    if scenario["car_speed"] == "over":
        if scenario["time_of_day"] == "night":
            response = "You are over speed limit. Make sure you are able to stop whithin range of your headlights."   
        elif scenario["road_type"] == "highway":
            response = "You are over speed limit in a highway. If you can't see car's mirror, they can't see you."
        elif scenario["weather"] in ["snow", "rain"]:
            response = "Please slow down and keep a 6 to 8 seconds following distance due to bad weather."
        elif scenario["weather"] == "fog":
            response = "Please slow down and turn on fog lights."
        else:
            response = random.choice(["Car speed is over speed limit.", "You are over the speed limit, please slow down."])

    if scenario["car_speed"] == "under":
        response = random.choice(["Please pick up the past to reach minimum speed limit if it's safe.", "Car speed under speed limit."])
    else:
        response = "Please stay within speed limit."
    return response

def detect_bad_weather(scenario):
    if scenario["weather"] == "fog":
        response = "Turn on fog lights."

    if scenario["weather"] in ["snow", "rain"]:
        response = "Keep a 6 to 8 seconds following distance due to bad weather."

    return response

def detect_distraction(scenario):
    
    if scenario["talking"] in ["talking", "yawning", "Yawning"] and scenario["driver_actions"] in ["phonecall_left", "phonecall_right"]:
        response = "Please use the car’s built-in audio to make phone calls."
   
    elif scenario["talking"] == "talking" and scenario["driver_actions"] not in ["phonecall_left","phonecall_right"]:
        
        #print("valuu", scenario["talking"])
        #print("valu", scenario["driver_actions"])
        response = random.choice(["Reminder to avoid charged conversations.", "Please keep conversations light hearted."])
    
    elif scenario["driver_actions"] == "drinking":
        response = "Please keep sips small."
    else:
        response = "Please avoid any distraction action while driving."
    return response

def detect_congestion(scenario):
    if scenario["traffic_density"] == "high" and scenario["road_type"] == "highway":
        response = "If you can't see car's mirror, they can't see you."

    elif scenario["traffic_density"] == "high":
        response = "Watch the front wheels of nearby cars to see if they are merging."

    elif scenario["traffic_density"] in ["low", "medium"] and scenario["time_of_day"] == "night" and scenario["road_type"] == ["rural", "highway"]:
        #if scenario["time_of_day"] == "night" and scenario["road_type"] in ["highway", "rural"]:
        response = "Make sure you are able to stop whithin range of your headlights."    
    else:
        response = "Please look 10 to 15 seconds ahead."
    return response
