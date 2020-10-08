# initros
# 
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:`pwd`

roslaunch motion_ctrl sim.launch 
roslaunch motion_ctrl base_navigation.launch 
