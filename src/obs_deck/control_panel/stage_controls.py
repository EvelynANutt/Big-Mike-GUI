""" Stage control """
import tkinter as tk
from primitives.number_input import NumberInput
from business.store import Store

class StageControlPanel:
    frame: tk.Frame

    def __init__(self, parent, store: Store):
        # Store the store
        self.store = store

        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Stage Controls', font=('Aria',26))

        # xyz translation and xy cropping names
        self.x_trans_input = NumberInput(self.frame, default_entry=self.store.attocube.xpos, title='x [nm]', 
                                         command_set_up=lambda: self.store.attocube.increment_up(0), 
                                         command_set_down=lambda: self.store.attocube.increment_down(0), 
                                         command_set_abs=lambda: self.store.attocube.move(0,0))
        self.y_trans_input = NumberInput(self.frame, default_entry=self.store.attocube.ypos, title='y [nm]', 
                                         command_set_up=lambda: self.store.attocube.increment_up(1), 
                                         command_set_down=lambda: self.store.attocube.increment_down(1), 
                                         command_set_abs=lambda: self.store.attocube.move(1,0))
        self.z_trans_input = NumberInput(self.frame, default_entry=self.store.attocube.zpos, title='z [nm]', 
                                         command_set_up=lambda: self.store.attocube.increment_up(2), 
                                         command_set_down=lambda: self.store.attocube.increment_down(2), 
                                         command_set_abs=lambda: self.store.attocube.move(2,0))

    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.x_trans_input.render()
        self.y_trans_input.render()
        self.z_trans_input.render()
        self.frame.pack(fill='both')