from morse.builder import *
from turtlebot_hospital_sim.Turtlebot import Turtlebot
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger

class GrabberRobot(Turtlebot):
    def __init__(self, name, path):
        Turtlebot.__init__(name=name, path=path)
        self.name = name
        self.path = path
        self.item_exchanger = ItemExchanger(name=name, obj="sphere")
