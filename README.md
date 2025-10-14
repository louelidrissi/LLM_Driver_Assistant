# LLM_Driver_Assistant

This Driver Assistant gives contextual advice and suggestions to drivers based on behavioral actions and physiological clues to determine driver's state with emphasis on distracted and drowsy states, as well as the context in which they happen (weather, speed according to speed limit, road type, time of the day). 

Dataset used is simulated based on a sample of Driver Monitoring Dataset ([DMD](https://dmd.vicomtech.org/)) for behavioral actions and physiological state of the driver to cover variety of scenarios and save storage space. Risk score is set to emphasis risky physiological states and behaviors. 

Assistant is trained using Angora free tier on Google Colab. Each description of driving instance and its environment is assumed to be 1sec long. To get one second instance of driver state labeled from DMD, set number of frames per labeled video to 50.
