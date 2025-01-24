""" Active cam control """
import tkinter as tk
from primitives.number_input import NumberInput

def move_x():
    print("booyah!")

class ActiveCamPanel:
    frame: tk.Frame

    def x_up(self):
        new_value = float(self.x_trans_input.value.get()) + 1
        self.x_trans_input.value.set(str(new_value))
        # Put attocube control code here!

    def x_down(self):
        new_value = float(self.x_trans_input.value.get()) - 1
        self.x_trans_input.value.set(str(new_value))

    def y_up(self):
        new_value = float(self.y_trans_input.value.get()) + 1
        self.y_trans_input.value.set(str(new_value))

    def y_down(self):
        new_value = float(self.y_trans_input.value.get()) - 1
        self.y_trans_input.value.set(str(new_value))

    def z_up(self):
        new_value = float(self.z_trans_input.value.get()) + 1
        self.z_trans_input.value.set(str(new_value))

    def z_down(self):
        new_value = float(self.z_trans_input.value.get()) - 1
        self.z_trans_input.value.set(str(new_value))
    
    ## def move_x_down(self):


    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Active Camera Controls', font=('Aria',26))

        # xyz translation and xy cropping names
        self.x_trans_input = NumberInput(self.frame, title='x [um]', command_plus=self.x_up, command_minus=self.x_down)
        self.y_trans_input = NumberInput(self.frame, title='y [um]', command_plus=self.y_up, command_minus=self.y_down)
        self.z_trans_input = NumberInput(self.frame, title='z [um]', command_plus=self.z_up, command_minus=self.z_down)
        """ When any of the + and - buttons are activated up or down,
        I want to move the microscope accordingly """


    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.x_trans_input.render()
        self.y_trans_input.render()
        self.z_trans_input.render()
        self.frame.pack(fill='both')