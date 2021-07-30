from morse.builder import *
import json
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger
from std_msgs.msg import String
import rospy
import time

def formatlog(severity, who, loginfo, skill, params):
    global simulation_init_time
    return ('['+severity+'],'+
               who+','+
               loginfo+','+
               skill+','+
               params)

class Nurse(Human):
    def __init__(self, name, path='human_rig'):
        Human.__init__(self, name=name, filename=path)
        self.name = name
        self.path = path
        self.pub = rospy.Publisher(f"{name}/fauth", String, queue_size=5)
        self.pub_action = rospy.Publisher(f"{name}/action", String, queue_size=5)
        self.pub_log = rospy.Publisher("/log", String, queue_size=5)
        self.pub_dum1 = rospy.Publisher("/nurse/comms", String, queue_size=5)
        self.pub_dum2 = rospy.Publisher("/led_strip/display", String, queue_size=5)
        
        self.sub = rospy.Subscriber("/led_strip/display", String, self.handle_auth)
        self.sub_comms = rospy.Subscriber("/nurse/comms", String, self.comms)
        self.item_exchanger = ItemExchanger(name=name, obj="cube")
        self.add_pose_sensor()

    def comms(self, com_data):
        pub_str = String()
        pub_str.data = "r1"
        self.sub_comms_new = rospy.Subscriber(f"{self.name}/comms", String, self.placeholder)
        rospy.logwarn(com_data)
        log = String()
        log.data = formatlog('info',
            self.name,
            'sync',
            'wait-message',
            '(status=message-received)')
        content = {
            'skill': 'wait-message',
            'status': 'message-received'
        }
        logdata = {
            'level': 'info',
            'entity': 'nurse',
            'content': content
        }
        log.data = json.dumps(logdata)
        print("NURSE")
        print(log.data)
        print(com_data.data)
        print("NURSE")
        self.pub_log.publish(log)
        # if com_data.data == "Open Drawer":
        self.pub_comms = rospy.Publisher(f"{self.name}/comms", String, queue_size=5)
        print(pub_str.data)
        rate = rospy.Rate(.5)
        for i in range(0,5):
            rospy.loginfo(pub_str)
            self.pub_comms.publish(pub_str)
            rate.sleep()

    def placeholder(self, com_data):
        print("foi")

    def add_pose_sensor(self):
        # Current position
        self.pose = Pose()
        self.pose.frequency(10)
        self.append(self.pose)
        self.pose.add_interface('ros', topic=f"{self.name}/pose", frame_id="map")

    def handle_auth(self, msg):
        pub_str = String()
        log = String()
        pub_str.data = "auth"
        self.pub.publish(pub_str)
        # log.data = self.name + ": athentication received "+str(pub_str)
        log.data = formatlog('info',
            self.name,
            'sync',
            'received-request',
            '(status=sending-request)')
        content = {
            'skill': 'athentication-request',
            'status': 'message-received'
        }
        logdata = {
            'level': 'info',
            'entity': 'nurse',
            'content': content
        }
        log.data = json.dumps(logdata)
        self.pub_log.publish(log)
        rate = rospy.Rate(.5)
        for i in range(0,10):
            rospy.loginfo(pub_str)
            self.pub.publish(pub_str)
            log.data = self.name + ": sent "+str(pub_str)
            rate.sleep()
        log.data = formatlog('info',
            self.name,
            'sync',
            'request-sent',
            '(status=waiting)')
        content = {
            'skill': 'athentication-sent',
            'status': 'waiting'
        }
        logdata = {
            'level': 'info',
            'entity': 'nurse',
            'content': content
        }
        log.data = json.dumps(logdata)
        self.pub_log.publish(log)
