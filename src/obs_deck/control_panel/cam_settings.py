""" Camera settings """
import tkinter as tk
from primitives.number_input import NumberInput

class CameraSettingsPanel:
    frame: tk.Frame

    def exposure_up(self):
        new_value = float(self.exposure_input.value.get()) + 1
        self.exposure_input.value.set(str(new_value))
        # Put attocube control code here!
        # include e.get() here? from entry

    def exposure_down(self):
        new_value = float(self.exposure_input.value.get()) - 1
        self.exposure_input.value.set(str(new_value))

    def frame_rate_up(self):
        new_value = float(self.frame_rate_input.value.get()) + 1
        self.frame_rate_input.value.set(str(new_value))

    def frame_rate_down(self):
        new_value = float(self.frame_rate_input.value.get()) - 1
        self.frame_rate_input.value.set(str(new_value))

    def cropping_up(self):
        new_value = float(self.cropping_input.value.get()) + 1
        self.cropping_input.value.set(str(new_value))

    def cropping_down(self):
        new_value = float(self.cropping_input.value.get()) - 1
        self.cropping_input.value.set(str(new_value))

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Camera Settings', font=('Aria',26))

        # Exposure, frame rate, and cropping names
        self.exposure_input = NumberInput(self.frame, title='Exposure time [ms]', command_plus=self.exposure_up, command_minus=self.exposure_down)
        self.frame_rate_input = NumberInput(self.frame, title='Frame rate [?]', command_plus=self.frame_rate_up, command_minus=self.frame_rate_down)
        self.cropping_input = NumberInput(self.frame, title='Cropping [?]', command_plus=self.cropping_up, command_minus=self.cropping_down)

    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.exposure_input.render()
        self.frame_rate_input.render()
        self.cropping_input.render()
        self.frame.pack(fill='both')