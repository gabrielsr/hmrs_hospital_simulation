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
# n_robots = 1
robot_list = []
for i in range(1, n_robots+1):
	robot_name = os.environ['ROBOT_NAME_'+str(i)]
	robot_pose = os.environ['ROBOT_POSE_'+str(i)][1:-1].split(';')
	dischar_rate = 0.0
	batt_state = os.environ['BATT_INIT_STATE_'+str(i)]
	if robot_name != os.environ['CHOSE_ROBOT']:
		dischar_rate = float(os.environ['BATT_SLOPE_STATE_'+str(i)]) / 10
	else:
		dischar_rate = float(os.environ['BATT_SLOPE_STATE_'+str(i)])
	print(robot_name+' has dischar_rate='+str(dischar_rate))
	robot = Turtlebot(name=robot_name, path=f"{PATH}/models/turtlebot.blend")
	robot.add_to_simulation(x=float(robot_pose[0]),
		y=float(robot_pose[1]),
		z_rot=float(robot_pose[2]),
		battery_discharge_rate=float(dischar_rate)/100.0,
		batt_init_state=float(batt_state)/100.0)
	robot_list.append(robot)

# Clock
clock = Clock()
clock.frequency(60)
robot_list[0].append(clock)
clock.add_interface('ros', topic="/clock")

# # Charging Zone
# charging_zone = Zone(type='Charging')
# charging_zone.size=[5 for x in range(3)]
# charging_zone.translate(x=-19, y=-3, z=0)

# lab_arm
arm = GrabberRobot(name="lab_arm", path=f"{PATH}/models/turtlebot.blend")
arm.add_to_simulation(x=-2.5, y=3, z_rot=0.0)

inventory = Inventory(name="Inventory", obj=None)

nurse_pose = os.environ['NURSE_POSE'][1:-1].split(';')
nurse = Nurse(name='nurse')
nurse.translate(x=float(nurse_pose[0]), y=float(nurse_pose[1]), z=0)

# set 'fastmode' to True to switch to wireframe mode
env = Environment(f'{PATH}/models/hospital_v5_v1.blend', fastmode=True)
env.set_horizon_color(color=(0.65, 0.65, 0.65))
env.simulator_frequency(120, 300, 300)
# env.simulator_frequency(60, 100, 100)
env.set_time_strategy(TimeStrategies.FixedSimulationStep)
# env.set_time_scale(slowdown_by = None, accelerate_by = 5)
env.use_vsync('OFF')
# env.use_internal_syncer()
env.set_camera_location([-2, -2, 5.0])
env.set_camera_rotation([1.09, 0, -0.7])

print('================================================')
print(os.environ['ROBOT_POSE_1'][1:-1].split(';'))
print('================================================')
