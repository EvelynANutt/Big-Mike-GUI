import cv2
from threading import Thread, Event, Lock
from typing import Callable
import PySpin
import time
import AMC
device=AMC.Device('192.168.1.1')
device.connect()

#these variables are for the xy positions of the upper left corner and lower right corner
fx1,fy1,fx2,fy2 = 740,713,942,793
current_z = device.control.getPositionsAndVoltages()[2]
device.move.setControlTargetPosition(2,steps[i])

class Attocube:
    def __init__(self):
        self.xpos = 1