from std_msgs.msg import String
from morse.builder import *
import rospy

class ItemExchanger:
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj
        self.sub = rospy.Subscriber(f"{name}/exchange", String, self.exchange)

    def exchange(self, robot):
        try:
            import bge
        except ImportError:
            # Game Engine is not loaded yet
            return
        scene = bge.logic.getCurrentScene()
        robot = scene.objects[robot.data]
        obj = scene.objects[self.obj]
        obj.worldPosition = [robot.worldPosition[0], robot.worldPosition[1], robot.worldPosition[2] + 0.5]
        obj.setParent(robot, True, False)
