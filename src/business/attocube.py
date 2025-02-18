import cv2
from threading import Thread, Event, Lock
from typing import Callable
import PySpin
import time
import AMC

# axis: [0|1|2] == [x|y|z]
#these variables are for the xy positions of the upper left corner and lower right corner
fx1,fy1,fx2,fy2 = 740,713,942,793

class Attocube:
    def __init__(self):
        self.device = AMC.Device('192.168.1.1')
        self.device.connect

        self.xpos = self.device.control.getPositionsAndVoltages()[0]
        self.ypos = self.device.control.getPositionsAndVoltages()[1]
        self.zpos = self.device.control.getPositionsAndVoltages()[2]

    def increment_up(self, dim):
        if (dim == 0):
            new_x = self.xpos + 1
            self.xpos = self.device.move.setControlTargetPosition(0, new_x)
        if (dim == 1):
            new_y = self.ypos + 1
            self.ypos = self.device.move.setControlTargetPosition(1, new_y)
        if (dim == 2):
            new_z = self.zpos + 1
            self.zpos = self.device.move.setControlTargetPosition(2, new_z)   

    def increment_down(self, dim):
        if (dim == 0):
            new_x = self.xpos - 1
            self.xpos = self.device.move.setControlTargetPosition(0, new_x)
        if (dim == 1):
            new_y = self.ypos - 1
            self.ypos = self.device.move.setControlTargetPosition(1, new_y)
        if (dim == 2):
            new_z = self.zpos - 1
            self.zpos = self.device.move.setControlTargetPosition(2, new_z)       

    def move(self, dim, absolute_pos):
        if (dim == 0):
            self.xpos = self.device.move.setControlTargetPosition(0, absolute_pos)
        if (dim == 1):
            self.ypos = self.device.move.setControlTargetPosition(1, absolute_pos)
        if (dim == 2):
            self.zpos = self.device.move.setControlTargetPosition(2, absolute_pos)