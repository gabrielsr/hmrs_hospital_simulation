from morse.builder import *
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger
from std_msgs.msg import String
import rospy
import time

class Nurse(Human):
    def __init__(self, name, path='human_rig'):
        Human.__init__(self, name=name, filename=path)
        self.name = name
        self.path = path
        self.pub = rospy.Publisher(f"{name}/fauth", String, queue_size=10)
        self.pub_action = rospy.Publisher(f"{name}/action", String, queue_size=10)
        self.pub_log = rospy.Publisher(f"{name}/log", String, queue_size=10)
        self.pub_dum = rospy.Publisher("/nurse/comms", String, queue_size=10)
        self.pub_dum = rospy.Publisher("/led_strip/display", String, queue_size=10)
        
        self.sub = rospy.Subscriber("/led_strip/display", String, self.handle_auth)
        self.sub_comms = rospy.Subscriber("/nurse/comms", String, self.comms)
        self.item_exchanger = ItemExchanger(name=name, obj="cube")
        self.add_pose_sensor()

    def comms(self, com_data):
        rospy.logwarn(com_data)
        log = String()
        log.data = self.name + ": received "+str(com_data)
        print("NURSE")
        print(log.data)
        print(com_data.data)
        print("NURSE")
        self.pub_log.publish(str(log))
        pub_str = String()
        # if com_data.data == "Open Drawer":
        pub_str.data = "deposit"
        print(pub_str.data)
        rate = rospy.Rate(1)
        for i in range(0,5):
            rospy.loginfo(pub_str)
            self.pub_action.publish(pub_str)
            rate.sleep()

    def add_pose_sensor(self):
        # Current position
        self.pose = Pose()
        self.pose.frequency(10)
        self.append(self.pose)
        self.pose.add_interface('ros', topic=f"{self.name}/pose", frame_id="map")

    def handle_auth(self, msg):
        pub_str = String()
        pub_str.data = "auth"
        self.pub.publish(pub_str)
        log.data = self.name + ": received "+str(pub_str)
        self.pub_log.publish(str(log))
        rate = rospy.Rate(1)
        for i in range(0,5):
            rospy.loginfo(pub_str)
            self.pub.publish(pub_str)
            log.data = self.name + ": sent "+str(pub_str)
            self.pub_log.publish(str(log))
            rate.sleep()
