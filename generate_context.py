import random


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

env_mapping = {
    "road_type": ["highway", "urban", "rural"],
    "weather": ["clear", "rain", "fog", "snow"],
    "time_of_day": ["morning", "afternoon", "evening", "night"],
    "traffic_density": ["low", "medium", "high"],
    "car_speed": ["none", "under", "over", "severe_over"]
}

action_state = "duration"

attention_state = {
    "objects_in_scene" : "duration",
    "hand_on_gear": "duration",
    "hands_using_wheel": "duration",
    "talking": "frequency",
    "gaze_on_road": "duration",
    "eyes_state": ["duration","frequency"],
    "yawning": "frequency",
}

# Speed limits in mph '''
road_speed_limits = {
        "highway": (55, 75),
        "urban": (25, 45),
        "rural": (35, 70)
    }


def select_time_of_day(action, driver_state, danger_mode):
    ''' Time of day won't be related to other simulated meta data '''
    weights = [0.3, 0.2, 0.3, 0.1]  # morning, afternoon, evening, night

    # if yawning, shift toward afternoon/evening/night
    if driver_state["yawning"] in ["Yawning", "Yawning without hand"]:
        weights = [0.1, 0.4, 0.4, 0.1]

    # if danger mode, shift more toward afternoon/evening
    if danger_mode:
        weights = [weights[0],  # morning stays same
                   max(0.05, weights[1] + 0.1),  # afternoon +0.1
                   max(0.05, weights[2] + 0.1),  # evening +0.1
                   max(0.05, weights[3] - 0.1)]  # night reduced slightly
            
    total = sum(weights)

    if total > 0:
        weights = [w / total for w in weights]
    else:
        # fallback if all weights somehow became 0
        weights = [1 / len(weights)] * len(weights)    

    time_of_day = random.choices(["morning", "afternoon", "evening", "night"], weights=weights)[0]

    return time_of_day


def select_road_type(action, driver_state, danger_mode):
    ''' Road type will be the first variable to be determined depending on the driver's actions
        Suburban is accounted for in rural to simplify  '''
    
    action_weights = {
        "safe_drive": [0.6, 0.3, 0.1],          # mostly highway
        "standstill_or_waiting": [0.6, 0.3, 0.1],
        "hair_and_makeup": [0.1, 0.7, 0.2],     # mostly urban
        "change_gear": [0.1, 0.7, 0.2],
        "reach_side": [0.2, 0.5, 0.3],          # some highway, mostly urban
        "reach_backseat": [0.05, 0.5, 0.45],    # rare highway, split urban/rural
        "drinking": [0.3, 0.4, 0.3],            # balanced
        "texting_right": [0.2, 0.5, 0.3],
        "texting_left": [0.2, 0.5, 0.3],
        "phonecall_right": [0.4, 0.4, 0.2],     # highway & urban
        "phonecall_left": [0.4, 0.4, 0.2],
        "radio": [0.4, 0.4, 0.2], 
        "unclassified": [0.3, 0.5, 0.2]
    }

    if driver_state["yawning"] in ["Yawning", "Yawning without hand"]:
        w = action_weights[action]
        highway = min(1.0, w[0] + 0.2)       # increase highway weight
        urban = max(0.05, w[1] - 0.1)           # slightly reduce urban
        rural = max(0.05, w[2] - 0.1)           # slightly reduce rural
        action_weights[action] = [highway, urban, rural]

    if danger_mode:
        w = action_weights[action]
        # increase "highway" for more dangerous actions
        if action in ["hair_and_makeup", "change_gear", "reach_side", "drinking", 
                        "texting_right", "texting_left", "phonecall_right", "phonecall_left", "radio"]:
            highway = min(1.0, w[0] + 0.2)       # increase highway weight
            urban = max(0.05, w[1] - 0.1)           # slightly reduce urban
            rural = max(0.05, w[2] - 0.1)           # slightly reduce rural
            action_weights[action] = [highway, urban, rural]

        # safe_drive and standstill_or_waiting: keep mostly same or slightly reduce rural
        elif action in ["safe_drive", "standstill_or_waiting"]:
            highway = min(1.0, w[0] + 0.1)
            urban = max(0.05, w[1] - 0.05)
            rural = max(0.05, w[2] - 0.05)
            action_weights[action] = [highway, urban, rural]

        # backseat reaching: already low highway, keep it low
        elif action == "reach_backseat":
            highway = w[0]  # keep very low
            urban = min(1.0, w[1] + 0.05)
            rural = max(0, w[2] - 0.05)
            action_weights[action] = [highway, urban, rural]

    weights = action_weights[action]
    total = sum(weights)
    if total > 0:
        weights = [w / total for w in weights]
    else:
        # fallback if all weights somehow became 0
        weights = [1 / len(weights)] * len(weights)  

    
    road_type = random.choices(env_mapping["road_type"], weights=weights)[0]

    return road_type


def select_weather(road_type, time_of_day, danger_mode):
    # Base probabilities
    weather_options = ["clear", "rain", "fog", "snow"]
    weights = [0.7, 0.15, 0.1, 0.05]  # default for safe mode

    if danger_mode:
        # shift towards riskier weather
        weights = [0.4, 0.3, 0.2, 0.1]

    # adjust for road_type
    if road_type == "rural":
        weights[2] += 0.1  # more fog
        weights[3] += 0.05  # slightly more snow
        weights[0] = max(0.05, weights[0]-0.15)  # less clear
    elif road_type == "highway":
        weights[1] += 0.1  # more rain on highway
        weights[0] = max(0.05, weights[0]-0.1)
    # urban: mostly unchanged

    # adjust for time_of_day
    if time_of_day in ["morning", "evening", "night"]:
        weights[2] += 0.05  # fog more likely in dim light
        weights[0] = max(0.05, weights[0]-0.05)

    # normalize weights to sum to 1
    total = sum(weights)
    weights = [w/total for w in weights]

    weather = random.choices(weather_options, weights=weights)[0]
    return weather


def select_traffic_density(road_type, weather, danger_mode):
    ''' Traffic density will relate to road type & weather '''
    
    if danger_mode:
        # Mostly high traffic for training (high-risk)
        weights = [0.1, 0.3, 0.6]  # low, medium, high
    else:
        # Testing: more realistic distribution
        if road_type == "highway":
            weights = [0.5, 0.35, 0.15]  # more low/medium, less high
        elif road_type == "urban":
            weights = [0.25, 0.5, 0.25]  # balanced
        else:  # rural
            weights = [0.35, 0.45, 0.2]  # realistic

    # Adjust for bad weather
    if weather in ["rain", "fog", "snow"]:
        # Shift low → medium traffic
        if danger_mode:
            shift = min(0.2, weights[0]-0.05)  # training: bigger shift
        else:
            shift = min(0.1, weights[0]-0.05)  # testing: smaller shift
        weights[0] -= shift
        weights[1] += shift

    weights = [max(0.05, w) for w in weights]

    # normalize weights to sum to 1
    total = sum(weights)
    weights = [w / total for w in weights]

    traffic_density = random.choices(["low", "medium", "high"], weights=weights)[0]
    return traffic_density

def select_car_speed(road_type, traffic_density, danger_mode):
    ''' Speed depends on road type & traffic density '''
    car_speed_range = road_speed_limits[road_type]

    if danger_mode:
        # danger mode → more extreme spread (overspeed + occasional underspeed)
        car_speed_limits = (car_speed_range[0] - 5, car_speed_range[1] + 25)
        overspeed_chance = 0.55  # more than half overspeed
        underspeed_chance = 0.25  # sometimes slower than flow
    else:
        # realistic: mostly within limits, few underspeeds, rare overspeeds
        car_speed_limits = (car_speed_range[0], car_speed_range[1] + 8)
        overspeed_chance = 0.1
        underspeed_chance = 0.2

    # Adjust for traffic 
    if traffic_density == "medium":
        # reduce upper limit moderately
        car_speed_limits = (max(10, car_speed_limits[0] - 3), car_speed_limits[1] - 5)
    elif traffic_density == "high":
        # reduce both ends more strongly
        car_speed_limits = (max(10, car_speed_limits[0] - 5), car_speed_limits[1] - 10)

    r = random.random()
    if r < underspeed_chance:
        # go below min limit slightly
        car_speed = max(10, car_speed_range[0] - random.randint(2, 8))
    elif r < underspeed_chance + overspeed_chance:
        # overspeed above max limit
        car_speed = min(130, car_speed_range[1] + random.randint(3, 20))
    else:
        # in-range normal behavior
        car_speed = random.randint(car_speed_range[0], car_speed_range[1])

    return car_speed


def speed_difference(road_type, weather, car_speed, traffic_density):
    car_speed_limits = road_speed_limits[road_type]
    speed_type = "none"

    if car_speed < car_speed_limits[0]:
        #car_speed_limits[0] - car_speed
        speed_type = "under"
        return speed_type 
    elif car_speed > car_speed_limits[1]:
        diff = car_speed - car_speed_limits[1]
        # Mark as more severe if weather or traffic make it worse
        if weather in ["rain", "fog", "snow"] or traffic_density == "high" or diff > 10:
            speed_type = "severe_over"
            return speed_type
        else:
            speed_type = "over"
            return speed_type
    else:
        return "none"
    

def add_env_description(action, driver_state, mode):
    road_type = select_road_type(action, driver_state, mode)
    time_of_day = select_time_of_day(action, driver_state, mode)
    weather = select_weather(action, time_of_day, mode)
    traffic_density = select_traffic_density(road_type, weather, mode)
    car_speed_num = select_car_speed(road_type, traffic_density, mode)
    speed_diff_type = speed_difference(road_type, weather, car_speed_num, traffic_density)
    #print(speed_diff_type)

    driver_state.update({
        "road_type": road_type,
        "weather": weather,
        "time_of_day": time_of_day,
        "traffic_density": traffic_density,
        "car_speed": speed_diff_type
    })
    #print("driver_state", driver_state)
    return driver_state


def test_function1():
    action = "phonecall_right"


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

    #df = pd.read_csv("driver_actions.csv")

    # Apply function to each row
    #driver_state["road_type"] = driver_state["driver_actions"].apply(select_road_type)

    # Save each dictionary as a row 
    #driver_state.to_csv("driver_actions_with_road.csv", index=False)
    #print(driver_state.head())

    road_type = select_road_type(action, driver_state, True)
    time_of_day = select_time_of_day(action, driver_state, True)
    weather = select_weather(action, time_of_day,True)
    traffic_density = select_traffic_density(road_type, weather, True)
    car_speed = select_car_speed(road_type, traffic_density, True)
    speed_diff_type = speed_difference(road_type, weather, car_speed, traffic_density)
    


    driver_state.update({
        "road_type": road_type,
        "weather": weather,
        "time_of_day": time_of_day,
        "traffic_density": traffic_density,
        "car_speed": speed_diff_type,
    })

    print(" ")

    print("driver_state 1 ", driver_state)

    print(" ")

    road_type = select_road_type(action, driver_state, False)
    time_of_day = select_time_of_day(action, driver_state, False)
    weather = select_weather(action, time_of_day, False)
    traffic_density = select_traffic_density(road_type, weather,False)
    car_speed = select_car_speed(road_type, traffic_density, False)
    speed_diff_type = speed_difference(road_type, weather, car_speed, traffic_density)

    #print("road_type", road_type)
    #print("weather", weather)
    #print("time_of_day", time_of_day)
    #print("traffic_density", traffic_density)
    #print("car_speed", car_speed)
    #print("speed range", road_speed_limits[road_type])
    #print("speed_difference", speed_diff_type, speed_diff)

    driver_state.update({
        "road_type": road_type,
        "weather": weather,
        "time_of_day": time_of_day,
        "traffic_density": traffic_density,
        "car_speed": speed_diff_type
    })

    print("driver_state 2 ", driver_state)
    return

def test_function2():
    action = "drinking"

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
    print(" ")

    road_type = select_road_type(action, driver_state, True)
    time_of_day = select_time_of_day(action, driver_state, True)
    weather = select_weather(action, time_of_day,True)
    traffic_density = select_traffic_density(road_type, weather, True)
    car_speed = select_car_speed(road_type, traffic_density, True)
    speed_diff_type = speed_difference(road_type, weather, car_speed, traffic_density)

    driver_state.update({
        "road_type": road_type,
        "weather": weather,
        "time_of_day": time_of_day,
        "traffic_density": traffic_density,
        "car_speed": speed_diff_type
    })

    print("driver_state 3 ", driver_state)

    road_type = select_road_type(action, driver_state, False)
    time_of_day = select_time_of_day(action, driver_state, False)
    weather = select_weather(action, time_of_day, False)
    traffic_density = select_traffic_density(road_type, weather,False)
    car_speed = select_car_speed(road_type, traffic_density, False)
    speed_diff_type = speed_difference(road_type, weather, car_speed, traffic_density)
    
    driver_state.update({
        "road_type": road_type,
        "weather": weather,
        "time_of_day": time_of_day,
        "traffic_density": traffic_density,
        "car_speed": speed_diff_type
    })

    print(" ")

    print("driver_state 4 ", driver_state)

    
    return

#test_function1()
#test_function2()