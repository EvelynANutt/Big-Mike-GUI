import cv2
from threading import Thread, Event, Lock
from typing import Callable
import PySpin
import time
from . import AMC
import time

# axis: [0|1|2] == [x|y|z]
#these variables are for the xy positions of the upper left corner and lower right corner
fx1,fy1,fx2,fy2 = 740,713,942,793

# Global variable for stage movement: Set to 1000nm = 1um
scale = 1000

class Attocube:
    def __init__(self):
        self.device = AMC.Device('192.168.1.1')
        self.device.connect()

        response = self.device.control.getPositionsAndVoltages()[0]
        print("Device response: ", response)
        self.xpos = self.device.control.getPositionsAndVoltages()[0]
        self.ypos = self.device.control.getPositionsAndVoltages()[1]
        self.zpos = self.device.control.getPositionsAndVoltages()[2]

        if self.xpos is None:
            self.xpos = 0 # Default value
        if self.ypos is None:
            self.ypos = 0 # Default value
        if self.zpos is None:
            self.zpos = 0 # Default value

    def increment_up(self, dim):
        if (dim == 0):
            new_x = self.xpos + scale
            time.sleep(1)
            self.device.move.setControlTargetPosition(0, new_x)
            time.sleep(1)
            self.xpos = self.device.control.getPositionsAndVoltages()[0]
        if (dim == 1):
            new_y = self.ypos + scale
            time.sleep(1)
            self.device.move.setControlTargetPosition(1, new_y)
            time.sleep(1)
            self.ypos = self.device.control.getPositionsAndVoltages()[1]
        if (dim == 2):
            new_z = self.zpos + scale
            time.sleep(1)
            self.device.move.setControlTargetPosition(2, new_z)
            time.sleep(1)
            self.zpos = self.device.control.getPositionsAndVoltages()[2]   

    def increment_down(self, dim):
        if (dim == 0):
            new_x = self.xpos - scale
            time.sleep(1)
            self.device.move.setControlTargetPosition(0, new_x)
            time.sleep(1)
            self.xpos = self.device.control.getPositionsAndVoltages()[0]
        if (dim == 1):
            new_y = self.ypos - scale
            time.sleep(1)
            self.device.move.setControlTargetPosition(1, new_y)
            time.sleep(1)
            self.ypos = self.device.control.getPositionsAndVoltages()[1]
        if (dim == 2):
            new_z = self.zpos - scale
            time.sleep(1)
            self.device.move.setControlTargetPosition(2, new_z) 
            time.sleep(1)
            self.zpos = self.device.control.getPositionsAndVoltages()[2]      

    def move(self, dim, absolute_pos):
        if (dim == 0):
            self.device.move.setControlTargetPosition(0, absolute_pos)
            time.sleep(1)
            self.xpos = self.device.control.getPositionsAndVoltages()[0]
        if (dim == 1):
            self.device.move.setControlTargetPosition(1, absolute_pos)
            time.sleep(1)
            self.ypos = self.device.control.getPositionsAndVoltages()[1]
        if (dim == 2):
            self.device.move.setControlTargetPosition(2, absolute_pos)
            time.sleep(1)
            self.zpos = self.device.control.getPositionsAndVoltages()[2]