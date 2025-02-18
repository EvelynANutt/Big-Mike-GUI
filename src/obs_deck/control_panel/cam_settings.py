""" Camera settings """
import tkinter as tk
from primitives.number_input import NumberInput
from business.store import Store

class CameraSettingsPanel:
    frame: tk.Frame

    def __init__(self, parent, store: Store):
        # Store the store
        self.store = store
        
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Camera Settings', font=('Aria',26))

        # Exposure, frame rate, and cropping names
        self.exposure_input = NumberInput(self.frame, default_entry=store.camera.exposure,  
                                          title='Exposure time [ms]', 
                                          command_set_up=self.update_exposure, 
                                          command_set_down=self.update_exposure, 
                                          command_set_abs=self.update_exposure)
        # self.frame_rate_input = NumberInput(self.frame, default_entry=store.camera.frame_rate,
        #                                     title='Frame rate [fps]', 
        #                                     command_set_up=self.update_frame_rate, 
        #                                     command_set_down=self.update_frame_rate, 
        #                                     command_set_abs=self.update_frame_rate)
        self.gain_input = NumberInput(self.frame, 
                                      title='Gain [dB]', default_entry=store.camera.gain,
                                      command_set_up=self.update_gain, 
                                      command_set_down=self.update_gain, 
                                      command_set_abs=self.update_gain)

    def update_exposure(self):
        value = float(self.exposure_input.value.get())
        self.store.camera.set_exposure_value(value)

    # def update_frame_rate(self):
    #     value = float(self.frame_rate_input.value.get())
    #     print(value)
    #     self.store.camera.set_frame_rate_value(value)

    def update_gain(self):
        value = float(self.gain_input.value.get())
        self.store.camera.set_gain_value(value)

    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.exposure_input.render()
        # self.frame_rate_input.render()
        self.gain_input.render()
        self.frame.pack(fill='both')