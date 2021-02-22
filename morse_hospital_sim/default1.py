#! /usr/bin/env morseexec

# Morse simulation for hospital with a turtlebot
# Run with morse run turtlebot_hospital_sim after starting ros with roscore

from morse.builder import *
from turtlebot_hospital_sim.Turtlebot import Turtlebot
from turtlebot_hospital_sim.Door import Door
from math import pi


PATH = "/".join(__file__.split("/")[:-1])

robot1 = Turtlebot(name='turtlebot1')
robot1.add_to_simulation(x=1.5, y=0)

# Clock
clock = Clock()
robot1.append(clock)
clock.add_interface('ros', topic="/clock")

robot2 = Turtlebot(name='turtlebot2')
robot2.add_to_simulation(x=1, y=0)

#door1 = Door(turn_angle=pi/2, x=0, y=0, z_rot=pi/2)
# door1 = Door(turn_angle=pi/2, x=0.56, y=-0.95, z_rot=pi/2, name="door1")
# door2 = Door(turn_angle=pi/2, x=1.56, y=-0.95, z_rot=pi/2, name="door2")
# door3 = Door(turn_angle=pi/2, x=-0.44, y=-0.95, z_rot=pi/2, name="door3")
# door4 = Door(turn_angle=pi/2, x=-1.39, y=-0.95, z_rot=pi/2, name="door4")

# Charging Zone
charging_zone = Zone(type='Charging')
charging_zone.size=[1 for x in range(3)]
charging_zone.translate(x=-1, y=-1, z=0)

# set 'fastmode' to True to switch to wireframe mode
env = Environment(f'{PATH}/models/Hospital.blend', fastmode=False)
env.set_horizon_color(color=(0.65, 0.65, 0.65))
env.set_camera_location([-3.0, -10, 20])
env.set_camera_rotation([1.09, 0, -1.27])
