import random
from generate_state_detection import (detect_high_speed, 
                                   detect_high_distraction, 
                                   detect_drowsiness, 
                                   detect_distraction, 
                                   detect_speed, 
                                   detect_bad_weather, 
                                   detect_congestion)


''' 
    Assumption: Object appearing alone does not generate an advice. 
                For now, it is accounted for in driver's actions

'''

def get_advice(scenario):
    # Check for combined high-risk scenarios
    advice = []

    if scenario["driver_actions"] == "standstill_or_waiting":
            advice = [random.choice(["Keep your wheels straight to avoid being pushed into another lane while waiting.", "Keep your eyes moving every 2 or 3 seconds when you start driving."])]

    elif scenario["car_speed"] == "severe_over" and scenario["classification"] == "distraction,drowsiness,high_distraction":
        advice1 = detect_high_speed(scenario)
        advice2 = detect_high_distraction(scenario)
        advice3 = detect_drowsiness(scenario)
        advice.extend([advice1, advice2, advice3])

    elif scenario["car_speed"] == "severe_over" and scenario["classification"] == "drowsiness,high_distraction":
        advice2 = detect_high_distraction(scenario)
        advice1 = detect_high_speed(scenario)
        advice3 = detect_drowsiness(scenario)
        advice.extend([advice1, advice2, advice3])

    elif scenario["car_speed"] == "severe_over" and  scenario["classification"] == "distraction,high_distraction":
        advice2 = detect_high_distraction(scenario)
        advice1 = detect_high_speed(scenario)
        advice3 = detect_distraction(scenario)
        advice.extend([advice1, advice2, advice3])

    elif scenario["car_speed"] == "severe_over" and scenario["classification"] == "distraction,drowsiness":
        advice1 = detect_high_speed(scenario)
        advice2 = detect_drowsiness(scenario)
        advice3 = detect_distraction(scenario)
        advice.extend([advice1, advice2, advice3])

    elif scenario["car_speed"] == "severe_over" and scenario["classification"] == "high_distraction":
        #advice.append("Stay focused and slow down — distractions at high speed are deadly.")
        advice2 = detect_high_distraction(scenario)
        advice1 = detect_high_speed(scenario)
        advice.extend([advice1, advice2])

    elif scenario["car_speed"] == "severe_over" and scenario["classification"] == "drowsiness":
        #advice.append("Slow down and take a rest if feeling drowsy.")
        advice1 = detect_high_speed(scenario)
        advice2 = detect_drowsiness(scenario)
        advice.extend([advice1, advice2])

    elif scenario["classification"] == "distraction,drowsiness,high_distraction":
        advice1 = detect_high_distraction(scenario)
        advice2 = detect_drowsiness(scenario)
        advice3 = detect_distraction(scenario)
        advice.extend([advice1, advice2, advice3])

    elif scenario["classification"] == "drowsiness,high_distraction":
        advice1 = detect_high_distraction(scenario)
        advice2 = detect_drowsiness(scenario)
        advice.extend([advice1, advice2])
    
    elif scenario["classification"] == "distraction,high_distraction":
        advice1 = detect_high_distraction(scenario)
        advice2 = detect_distraction(scenario)
        advice.extend([advice1, advice2])
    
    elif scenario["classification"] == "distraction,drowsiness":
        advice1 = detect_drowsiness(scenario)
        advice2 = detect_distraction(scenario)
        advice.extend([advice1, advice2])
    
    elif scenario["weather"] in ["rain", "snow", "fog"] and scenario["car_speed"] == "over":
        #advice.append("Reduce speed and drive carefully in adverse weather.")
        advice1 = detect_speed(scenario)
        advice2 = detect_bad_weather(scenario)
        advice.extend([advice1, advice2])

    elif scenario["classification"] == "high_distraction" and scenario["traffic_density"] in ["high", "medium"]:
        #advice.append("Focus on the road and keep a safe distance in traffic.")
        advice1 = detect_high_distraction(scenario)
        advice2 = detect_congestion(scenario)
        advice.extend([advice1, advice2])

    elif scenario["classification"] == "drowsiness" and scenario["traffic_density"] in ["high", "medium"]:
        #advice.append("Keep your distance, slow down, or pull over if tired.")
        advice1 = detect_drowsiness(scenario)
        advice2 = detect_congestion(scenario)
        advice.extend([advice1, advice2])

    else: # Handle individual risks here
        
        # over speeding 
        if scenario["car_speed"] == "severe_over":
            advice = [detect_high_speed(scenario)]
        
        elif scenario["classification"] == "high_distraction":
            advice = [detect_high_distraction(scenario)]

        # drowsiness
        elif scenario["classification"] == "drowsiness":
            advice = [detect_drowsiness(scenario)]

        # disctraction
        elif scenario["classification"] == "distraction":
            advice = [detect_distraction(scenario)]

        # speed
        elif scenario["car_speed"] in ["over", "under"]:
            advice = [detect_speed(scenario)]

        # traffic
        elif scenario["traffic_density"] in ["high", "medium"]:
            advice = [detect_congestion(scenario)]

        elif scenario["traffic_density"] == "low" and scenario["time_of_day"] == "night" and scenario["road_type"] == "rural":
            advice = ["Make sure you are able to stop whithin range of your headlights."] 
        
        # weather
        elif scenario["weather"] in ["rain", "snow", "fog"]:
            advice = [detect_bad_weather(scenario)]

        #road type
        elif scenario["road_type"] == "highway":
            advice = ["Avoid fast lane unless actively passing."]

        elif scenario["road_type"] == "urban":
            advice = ["Check mirrors every 5 to 8 seconds."]

        elif scenario["road_type"] == "rural":
            advice = ["Use peripheral vision actively to detect subtle movements along the roadside."]
            
        elif scenario["driver_actions"] ==  "safe_drive" and scenario["car_speed"] == "none":
            advice = ["Keep your eyes moving every 2 or 3 seconds."]
        else:
            advice = ["Keep your eyes moving every 2 or 3 seconds."]
    return advice
