""" Stage control """
import tkinter as tk
from primitives.number_input import NumberInput

class StageControlPanel:
    frame: tk.Frame

    def command_set_x(self):
        print(self.x_trans_input.value.get())
        # Put attocube control code here!

    def command_set_y(self):
        print(self.y_trans_input.value.get())
        # Put attocube control code here!
            
    def command_set_z(self):
        print(self.z_trans_input.value.get())
        # Put attocube control code here!

    def __init__(self, parent, store):
        # Store the store
        self.store = store
        
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Stage Controls', font=('Aria',26))

        # xyz translation and xy cropping names
        self.x_trans_input = NumberInput(self.frame, title='x [um]', command_set=self.command_set_x)
        self.y_trans_input = NumberInput(self.frame, title='y [um]', command_set=self.command_set_y)
        self.z_trans_input = NumberInput(self.frame, title='z [um]', command_set=self.command_set_z)

    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.x_trans_input.render()
        self.y_trans_input.render()
        self.z_trans_input.render()
        self.frame.pack(fill='both')