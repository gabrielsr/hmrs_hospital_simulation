from morse.builder import *
from std_msgs.msg import String
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger
import rospy

PATH = "/".join(__file__.split("/")[:-3])

class Inventory:
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj
        self.logger_pub = rospy.Publisher("/log", String, queue_size=1)
        self.sub = rospy.Subscriber(f"{name}/exchange", String, self.exchange)
        self.sub_i = rospy.Subscriber(f"/inventory", String, self.inventory_callback)

    def exchange(self, robot):
        try:
            import bge
        except ImportError:
            # Game Engine is not loaded yet
            return
        # TODO log the  
        scene = bge.logic.getCurrentScene()
        robot = scene.objects[robot.data]
        obj = scene.objects[self.obj]
        obj.worldPosition = [robot.worldPosition[0], robot.worldPosition[1], robot.worldPosition[2] + 0.5]
        obj.setParent(robot, True, False)
        log = String()
        log.data = "Inventory received object: " + str(robot.data)
        self.logger_pub.publish(log)

    def inventory_callback(self, msg):
        log = String()
        log.data = "Sample has arrived at " + str(rospy.get_rostime())
        self.logger_pub.publish(log)
        rospy.loginfo(self.name+": received "+msg.data)
        self.logger_pub.publish(msg)
        log.data = "Trigger simulation ending ..."
        self.logger_pub.publish(log)
        log.data = "ENDSIM"
        self.logger_pub.publish(log)
