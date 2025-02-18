from threading import Thread, Event, Lock
from typing import Callable
import time
from . import AMC
import time

# axis: [0|1|2] == [x|y|z]
#these variables are for the xy positions of the upper left corner and lower right corner
fx1,fy1,fx2,fy2 = 740,713,942,793

# Global variable for stage movement: Set to 1000nm = 1um

class Attocube:
    def __init__(self):
        self.device = AMC.Device('192.168.1.1')
        self.device.connect()

    def get_value(self, dim: int) -> float:
        value = self.device.control.getPositionsAndVoltages()[dim]
        if value is None:
            return 0.0
        else:
            return value

    def set_value(self, dim: int, new_value: float):
        self.device.move.setControlTargetPosition(dim, new_value)