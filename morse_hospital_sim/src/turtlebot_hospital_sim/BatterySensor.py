import rospy
import os
from threading import Timer
from morse.builder import *
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import Twist

def formatlog(severity, who, loginfo, skill, params):
    global simulation_init_time
    return ('['+severity+'],'+
               who+','+
               loginfo+','+
               skill+','+
               params)


class BatterySensor:
    def __init__(self, parent,
            capacity=1800,
            initial_percentage=1,
            discharge_rate_percentage=0.0005,
            discharge_rate_ah=0):
        self.parent = parent
        self.capacity = 1800
        self.percentage = initial_percentage
        self.voltage = 11.1
        self.status = 0
        self.health = 0
        self.tech = 3
        self.current = 0.8
        self.design_capacity = 1800
        self.discharge_rate_ah = discharge_rate_ah
        self.discharge_rate_percentage = discharge_rate_percentage

        self.charge = capacity*initial_percentage

        self.battery_pub = rospy.Publisher(f"{self.parent}/battery", BatteryState, queue_size=1)
        self.log_pub = rospy.Publisher(f"/log", String, queue_size=1)
        self.vel_pub = rospy.Publisher(f"{self.parent}/cmd_vel", Twist, queue_size=1)

        self.thr_timer = Timer(30, self.set_ros_timer)
        self.thr_timer.start()

    def set_ros_timer(self):
        while rospy.get_time() == 0:
            rospy.logwarn(f"{self.parent} waiting for clock...")
        rospy.logwarn(f"{self.parent} setting up battery module...")
        self.timer = rospy.Timer(rospy.Duration(1), self.update_charge)
        self.logtimer = rospy.Timer(rospy.Duration(5), self.update_log)

    def update_log(self, event):
        if self.parent == os.environ['CHOSE_ROBOT']:
            log = String()
            log.data = f'{self.parent}_battery_level={self.percentage}'
            self.log_pub.publish(log)

    def update_charge(self, event):
        msg = BatteryState()
        msg.voltage = self.voltage
        msg.current = self.current
        msg.capacity = self.capacity
        msg.design_capacity = self.design_capacity
        msg.power_supply_status = self.status
        msg.power_supply_health = self.health
        msg.power_supply_technology = self.tech
        msg.present = True

        msg.charge = self.charge - self.discharge_rate_ah if self.discharge_rate_ah != 0 else self.charge - self.discharge_rate_percentage*self.capacity
        msg.percentage = self.charge/self.capacity
        rospy.logwarn(f"{self.parent} updating charge battery {msg.percentage*100}%...")
        self.battery_pub.publish(msg)
        self.charge = msg.charge
        self.percentage = msg.percentage
        if msg.percentage < .05:
            if self.parent == os.environ['CHOSE_ROBOT']:
                rospy.logwarn(f"{self.parent} requesting simulation end...")
                log = String()
                log.data = "ENDLOWBATT"
                self.log_pub.publish(log)
            self.new_timer = rospy.Timer(rospy.Duration(1.0/100.0), self.stop_robot)
            # self.timer.cancel()
            self.timer.shutdown()
            # return

    def stop_robot(self, event):
        vel_0 = Twist()
        self.vel_pub.publish(vel_0)
        # check if the robot has to shutdown the simulation when low batt
