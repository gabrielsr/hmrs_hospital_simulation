import rospy
from threading import Timer
from morse.builder import *
from sensor_msgs.msg import BatteryState

class BatterySensor:
    def __init__(self, parent, capacity=1800, initial_percentage=1, discharge_rate_percentage=0.05, discharge_rate_ah=0):
        self.parent = parent
        self.capacity = capacity * initial_percentage
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

        self.timer = Timer(1, self.update_charge)
        self.timer.start()


    def update_charge(self):
        try:
            msg = BatteryState()
            msg.voltage = self.voltage
            msg.current = self.current
            msg.capacity = self.capacity
            msg.design_capacity = self.design_capacity
            msg.power_supply_status = self.status
            msg.power_supply_health = self.health
            msg.power_supply_technology = self.tech
            msg.present = True

            msg.charge = self.charge - self.discharge_rate_ah if self.discharge_rate_ah != 0 else self.charge - self.charge*self.discharge_rate_percentage
            msg.percentage = self.charge/self.capacity
            self.battery_pub.publish(msg)
            self.charge = msg.charge
            self.percentage = msg.percentage
        except rospy.exceptions.ROSException:
            pass
        self.timer = Timer(1, self.update_charge)
        self.timer.start()
