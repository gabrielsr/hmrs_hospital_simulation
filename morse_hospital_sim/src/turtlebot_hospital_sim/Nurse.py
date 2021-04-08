from morse.builder import *
from ItemExchanger import ItemExchanger

class Nurse(Human):
    def __init__(self, name, path='human_rig'):
        Human.__init__(name=name, filename=path)
        self.name = name
        self.path = path
        self.item_exchanger = ItemExchanger(name=name, obj="cube")
