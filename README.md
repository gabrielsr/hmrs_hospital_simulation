# hmrs_hostpital_sim_morse

# Setup Dependencies
ros version m
sudo apt install ros-melodic-navigation
turtlebot3
pip install 

# 
For executing the simulation you need to 
1. Start a roscore
 `initros`
 `roscore`
2. Init simulator (you need to have it imported with 'morse import')
 morse run morse_hospital_sim
3. start clients see


# Simulation Single Robot in the Host Machine
 morse import morse_hospital_sim
 # cd .. 
 export ROS_PATH...
 # 
 ros run motion_ctrl sim.launch 
 ros run motion_ctrl base_navigation.launch 


