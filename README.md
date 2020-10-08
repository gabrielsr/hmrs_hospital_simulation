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
1. Start a roscore
2. Init simulation
 morse run morse_hospital_sim
3. start ros robots controllers

### Initing ros robot controllers
 # cd .. 
 export ROS_PATH...
 # 
 ros run motion_ctrl sim.launch 
 ros run motion_ctrl base_navigation.launch 


## Troubleshooting
