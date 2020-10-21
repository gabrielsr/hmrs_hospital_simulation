from morse.builder import *
import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose

PATH = "/".join(__file__.split("/")[:-3])


class Door(Robot):
    def __init__(self, turn_angle, x=0, y=0, z=0.1,
                 x_rot=0, y_rot=0, z_rot=0,
                 name="door", path=f"{PATH}/models/door.blend"):
        Robot.__init__(self, path, name)
        self.name = name
        self.path = path

        self.x = x
        self.y = y
        self.z = z
        self.x_rot = x_rot
        self.y_rot = y_rot
        self.z_rot = z_rot
        self.turn_angle = turn_angle
        self.translate(self.x-2.1, self.y+1.15, z)
        self.rotate(x_rot, y_rot, z_rot)

        self.teleport = Teleport()
        self.append(self.teleport)
        self.teleport.add_interface('ros', topic=f"{self.name}/teleport")

        self.sub = rospy.Subscriber(f"{self.name}/open", Bool, self.open_close)
        self.pub = rospy.Publisher(f"{self.name}/teleport", Pose, queue_size=1)

    def move(self, position, orientation):
        x, y, z = position
        x_rot, y_rot, z_rot = orientation
        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        pose.orientation.x = x_rot
        pose.orientation.y = y_rot
        pose.orientation.z = z_rot

        self.pub.publish(pose)

    def open_close(self, open):
        if open.data:
            position = (self.x + 0.38, self.y, self.z)
            orientation = (self.turn_angle, self.y_rot, self.z_rot)
        else:
            position = (self.x, self.y, self.z)
            orientation = (self.x_rot, self.y_rot, self.z_rot)
        self.move(position, orientation)
