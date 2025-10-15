# LLM_Driver_Assistant

This Driver Assistant gives contextual advice and suggestions to drivers based on behavioral actions and physiological clues (drinking, gaze on road, eye state, hand actions, yawning, talking, etc ...) to determine driver's state with emphasis on distracted and drowsy states, as well as the context in which they happen (weather, speed according to speed limit, road type, time of the day). 

Dataset used is simulated based on a sample of Driver Monitoring Dataset ([DMD](https://dmd.vicomtech.org/)) for behavioral actions and physiological state of the driver to cover variety of scenarios and save storage space. 

The risk score of each instance used is set to emphasis risky physiological states and behaviors. Each instance of simulated data and its context/environment is assumed to be 1sec long. Number of frames per labeled instance from DMD is set to 50 per second, each instance being 1 sec long. 

Assistant is trained using llama. Training dataset includes scenarios with higher risk_score, while testing dataset' scenarios are more realistic. 

