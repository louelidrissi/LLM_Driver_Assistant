# LLM_Driver_Assistant

This Driver Assistant gives contextual advice and suggestions to drivers based on behavioral actions and physiological clues (drinking, gaze on road, eye state, hand actions, yawning, talking, etc ...) to determine driver's state with emphasis on distracted and drowsy states and speed according to speed limit, as well as the context in which they happen (weather, road type, time of the day) as secondary factors. 

Dataset used is simulated based on a sample of Driver Monitoring Dataset ([DMD](https://dmd.vicomtech.org/)) for behavioral actions and physiological state of the driver to cover variety of scenarios and to save storage space. 

Each instance of simulated data and its context/environment is assumed to be 1sec long. Number of frames per labeled instance from DMD is set to 50 per second, each instance being 1 sec long. 

Assistant is trained using [Alpaca-LoRA](https://github.com/tloen/alpaca-lora/tree/8bb8579e403dc78e37fe81ffbb253c413007323f) on Google Colab. Training dataset includes scenarios with higher risk states and external factors, while testing dataset' scenarios are more realistic. 


