# Spatial_Audio_Communication

Required downloads: 
- HyperIMU android app
- Max 8 
- dearVR_MICRO (Spatial Audio Plug-in)

This is an in-progress project to render spatial audio when communicating between two different headsets. The project is written in python and uses Max 8 for the spatial audio plug-in. Phone sensors are used to collect orientation and location data. This project uses the HyperIMU android app. This project as it stands is for two way communication and requires a laptop or LattePanda to process and render spatial audio and headset with microphone for each individual. The spatial audio input script parses all necessary data, calculates necessary inputs, and sends inputs locally to plugin. Plugin and spatial audio input script must be running on both laptops. An audio streaming software was used and the output audio of the software should be routed through the input of the plugin to render spatial audio. The output of the plugin should then go directly into the headset for the user.
