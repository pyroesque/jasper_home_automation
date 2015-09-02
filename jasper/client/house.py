
from lights import Lights
from Tempmonitor import TempMonitor
from Door import Door

class House:

    def __init__(self,mic):
        self.lights = Lights()
        self.therm = TempMonitor()
        self.door = Door(mic)
        