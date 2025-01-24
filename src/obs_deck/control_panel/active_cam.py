""" Active cam control """
import tkinter as tk
from primitives.number_input import NumberInput

def move_x():
    print("booyah!")

class ActiveCamPanel:
    frame: tk.Frame

    def move_up(self):
        new_value = float(self.x_trans_input.value.get()) + 1
        self.x_trans_input.value.set(str(new_value))
        print("U dah beast")

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Active Camera Controls', font=('Aria',26))

        # xyz translation and xy cropping names
        self.x_trans_input = NumberInput(self.frame, title='x [um]', command=self.move_up)
        self.y_trans_input = NumberInput(self.frame, title='y [um]', command=self.move_up)
        self.z_trans_input = NumberInput(self.frame, title='z [um]', command=self.move_up)
        """ When any of the + and - buttons are activated up or down,
        I want to move the microscope accordingly """


    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.x_trans_input.render()
        self.y_trans_input.render()
        self.z_trans_input.render()
        self.frame.pack(fill='both')