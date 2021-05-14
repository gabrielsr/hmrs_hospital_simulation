from morse.builder import *
from turtlebot_hospital_sim.Turtlebot import Turtlebot
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger

PATH = "/".join(__file__.split("/")[:-3])

class GrabberRobot(Turtlebot):
    def __init__(self, name, path=f"{PATH}/models/turtlebot.blend"):
        Turtlebot.__init__(self, name=name, path=path)
        self.name = name
        self.path = path
        self.item_exchanger = ItemExchanger(name=name, obj="sphere")
