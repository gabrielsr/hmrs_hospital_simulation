# hmrs_hostpital_sim_morse

## Install Dependencies
ros version m
sudo apt install ros-melodic-navigation
turtlebot3
pip install 

## Setup Environment
Import simulation 
 morse import morse_hospital_sim

Clone motion_ctrl
git clone ....


## Execution
For executing the simulation you need to 
1. In a terminal setup ros1 with 'initros'and then start 'roscore'

2. start ros robots controllers

3. In a another tertminal init the simulation

  morse run morse_hospital_sim

### Initing ros robot controllers
 # cd .. 
 export ROS_PATH...
 # 
 ros run motion_ctrl sim.launch 
 ros run motion_ctrl base_navigation.launch 


## Troubleshooting
. Command 'roscore' not found, but can be installed with:
  Check if you had executed 'initros' in the current terminal.
