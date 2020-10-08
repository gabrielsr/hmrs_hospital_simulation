# hmrs_hostpital_sim_morse

### Install Dependencies

. Install Morse
. Install ROS1
. Install Aditional Dependencies

```console
sudo apt install ros-melodic-navigation ros-melodic-navigation 
```

### Setup Environment
Import simulation 
```console
 morse import morse_hospital_sim

```

Clone motion_ctrl

```console

git clone ....

```

### Execution
For executing the simulation you need to 
1. In a terminal setup ros1 with 'initros' and then start 'roscore'
```console
initros
roscore

```

2. In another tertminal init the simulation
```console
initros
morse run morse_hospital_sim
```
3. Start ros robots controllers

#### Initing ros robot controllers
 # cd .. 
 export ROS_PATH...
 # 
 ros run motion_ctrl sim.launch 
 ros run motion_ctrl base_navigation.launch 


## Troubleshooting
. Command 'roscore' not found, but can be installed with:
  Check if you had executed 'initros' in the current terminal.

. No module named 'rospy' error in the beginning of the simulation.
  Check if you had executed 'initros' in the current terminal.
