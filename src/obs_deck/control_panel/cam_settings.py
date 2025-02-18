""" Camera settings """
import tkinter as tk
from primitives.number_input import NumberInput

class CameraSettingsPanel:
    frame: tk.Frame

    def __init__(self, parent, store):
        # Store the store
        self.store = store
        
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Camera Settings', font=('Aria',26))

        # Exposure, frame rate, and cropping names
        self.exposure_input = NumberInput(self.frame, title='Exposure time [ms]', command_set_up=None, 
                                          command_set_down=None, command_set_abs=None)
        self.frame_rate_input = NumberInput(self.frame, title='Frame rate [?]', command_set_up=None, 
                                            command_set_down=None, command_set_abs=None)
        self.cropping_input = NumberInput(self.frame, title='Cropping [?]', command_set_up=None, 
                                          command_set_down=None, command_set_abs=None)

    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.exposure_input.render()
        self.frame_rate_input.render()
        self.cropping_input.render()
        self.frame.pack(fill='both')