''' Input template '''

sentence_templates = {
    "classification": "{classification} detected.",
    "driver_actions": "Driver is {driver_actions}.",
    "car_speed": "Driver's car is {car_speed} the speed limit.",
    "gaze_on_road": "Driver is {gaze_on_road},",
    "eyes_state": "their eyes are {eyes_state},",
    "hands_using_wheel": "and {hands_using_wheel}.",
    "traffic_density": "Traffic is {traffic_density}",
    "road_type": "on {road_type}.",
    "yawning": "Driver is {yawning}.",
    "talking": "Driver is {talking}.",
    "weather": "{weather}",
    "time_of_day": "{time_of_day}."
    }

fill_template= {
    "safe_drive": "driving safely",
    "standstill_or_waiting": "standing still or waiting",
    "reach_side": "reaching to their side",
    "reach_backseat": "reaching to the backseat",
    "radio": "using the radio",
    "change_gear": "changing gear",
    "hair_and_makeup": "doing hair or make up",
    "drinking": "drinking",
    "texting_right": "texting with their right hand",
    "texting_left": "texting with their left hand",
    "phonecall_right": "making a phone call with their right hand",
    "phonecall_left": "making a phone call with their left hand",
    "unclassified": "doing an unclassified action",

    "both": "both hands are on the wheel",
    "only_left": "only the left hand is on the wheel", 
    "only_right": "only the right hand is on the wheel",     
    "none": "no hand is on the wheel", 
    "hand_on_gear": "one hand is on the gear",
    "hand_not_on_gear": "No hand is on the gear" ,

    "not_talking": "not talking",
    "talking": "talking",
    "not_yawning": "not yawning",
    "Yawning without hand": "yawning without their hand",
    "Yawning with hand": "yawning",
    "Yawning": "yawning",

    "looking_road": "looking at the road",
    "not_looking_road": "not looking at the road",

    "open": "open",
    "opening": "opening",
    "closing": "closing",
    "close": "closing",
    "undefined": "not clearly visible",

    "highway": "the highway",   
    "urban": "an urban road",    
    "rural": "a rural road",     

    "clear": "The weather is clear",
    "rain": "It is raining",      
    "fog": "It's foggy",     
    "snow": "It's snowing" ,      

    "morning": "this morning", 
    "afternoon": "this afternoon", 
    "evening": "this evening",  
    "night": "tonight",      

    "low": "light",      
    "medium": "moderate",
    "high": "heavy",       

    "within_speed_limit": "within",          
    "under": "under",          
    "over": "over",           
    "severe_over": "severely over",     

    "distraction": "Distraction",
    "drowsiness": "Drowsiness",
    "high_distraction": "Highly distracting action",

    "distraction,drowsiness": "Distraction and drowsiness",
    "distraction,high_distraction": "Two distracting actions",
    "drowsiness,high_distraction": "Highly distracting action and drowsiness",
    
    "distraction,drowsiness,high_distraction": "Two distracting actions and drowsiness",  
}

