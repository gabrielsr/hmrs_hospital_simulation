#! /usr/bin/env morseexec

# Morse simulation for hospital with a turtlebot
# Run with morse run turtlebot_hospital_sim after starting ros with roscore

from morse.builder import *
from turtlebot_hospital_sim.Turtlebot import Turtlebot
from turtlebot_hospital_sim.GrabberRobot import GrabberRobot
from turtlebot_hospital_sim.Nurse import Nurse
from turtlebot_hospital_sim.Inventory import Inventory
import os

PATH = "/".join(__file__.split("/")[:-1])

# robot_pose_1 = os.environ['ROBOT_POSE_1'][1:-1].split(';')
# robot1 = GrabberRobot(name='turtlebot1', path=f"{PATH}/models/turtlebot.blend")
# robot1.add_to_simulation(x=float(robot_pose_1[0]), y=float(robot_pose_1[1]))


# robot_pose_2 = os.environ['ROBOT_POSE_2'][1:-1].split(';')
# robot2 = GrabberRobot(name='turtlebot2', path=f"{PATH}/models/turtlebot.blend")
# robot2.add_to_simulation(x=float(robot_pose_2[0]), y=float(robot_pose_2[1]))

n_robots = int(os.environ['N_ROBOTS'])
robot_list = []
for i in range(1, n_robots+1):
	robot_name = os.environ['ROBOT_NAME_'+str(i)]
	robot_pose = os.environ['ROBOT_POSE_'+str(i)][1:-1].split(';')
	robot = GrabberRobot(name=robot_name, path=f"{PATH}/models/turtlebot.blend")
	robot.add_to_simulation(x=float(robot_pose[0]), y=float(robot_pose[1]), z_rot=float(robot_pose[2]))
	robot_list.append(robot)

# Clock
clock = Clock()
robot_list[0].append(clock)
clock.add_interface('ros', topic="/clock")

# Charging Zone
charging_zone = Zone(type='Charging')
charging_zone.size=[5 for x in range(3)]
charging_zone.translate(x=-19, y=-3, z=0)

nurse = Nurse(name='nurse')
nurse.translate(x=-35.97, y=17.67, z=0)

# set 'fastmode' to True to switch to wireframe mode
env = Environment(f'{PATH}/models/hospital_v3_v1.blend', fastmode=True)
env.set_horizon_color(color=(0.65, 0.65, 0.65))
env.show_framerate()
env.simulator_frequency(25)
# env.set_time_scale(20)
env.use_vsync('OFF')
env.use_internal_syncer()
env.set_camera_location([-2, -2, 5.0])
env.set_camera_rotation([1.09, 0, -0.7])

print('================================================')
print(os.environ['ROBOT_POSE_1'][1:-1].split(';'))
print('================================================')
