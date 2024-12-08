""" Active cam control """
import tkinter as tk
from primitives.number_input import NumberInput

class ActiveCamPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Active Camera Controls', font=('Aria',26))
        self.play_button = tk.Button(self.header, text='▶', font=('Aria',16))
        self.stop_button = tk.Button(self.header, text='⏹', font=('Aria',16))

        # xyz translation and xy cropping
        self.x_trans_input = NumberInput(self.frame, title='x [nm]')
        self.y_trans_input = NumberInput(self.frame, title='y [nm]')
        self.z_trans_input = NumberInput(self.frame, title='z [nm]')
        self.x_zoom_input = NumberInput(self.frame, title='x zoom')
        self.y_zoom_input = NumberInput(self.frame, title='y zoom')

    def render(self):
        self.title.pack(side='left', expand=True)
        self.play_button.pack(side='left')
        self.stop_button.pack(side='left')
        self.header.pack(fill='x')

        self.x_trans_input.render()
        self.y_trans_input.render()
        self.z_trans_input.render()
        self.x_zoom_input.render()
        self.y_zoom_input.render()
        self.frame.pack(fill='both')