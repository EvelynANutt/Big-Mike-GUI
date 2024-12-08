""" Experiment control """
import tkinter as tk

class ExperimentPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Experiment', font=('Aria',26))
        self.play_button = tk.Button(self.header, text='▶', font=('Aria',16))
        self.stop_button = tk.Button(self.header, text='⏹', font=('Aria',16))

        # Text for preset
        self.preset_name = tk.Label(self.frame, text='Preset: Calibration Test', font=('Aria',16))

    def render(self):
        self.title.pack(side='left', expand=True)
        self.play_button.pack(side='left')
        self.stop_button.pack(side='left')
        self.header.pack(fill='x')
        self.preset_name.pack(anchor='w')
        self.frame.pack(fill='both', pady=10)