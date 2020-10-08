# hmrs_hostpital_sim_morse

### Install Dependencies

* Install ROS1
 http://wiki.ros.org/kinetic/Installation/Ubuntu
* Install Aditional Dependencies
* Install Morse

```console
sudo apt install morse-simulator python3-morse-simulator
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
Note that motion_ctrl needs to be in ROS_PACKAGE_PATH

```console
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:`pwd`
roslaunch motion_ctrl sim.launch 
roslaunch motion_ctrl base_navigation.launch
```


## Troubleshooting
. Command 'roscore' not found, but can be installed with:
  Check if you had executed 'initros' in the current terminal.

. No module named 'rospy' error in the beginning of the simulation.
  Check if you had executed 'initros' in the current terminal.
