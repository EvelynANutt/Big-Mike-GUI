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
        self.stop_button = tk.Button(self.header, text='⏹', font=('Aria',18))
        self.reset_button = tk.Button(self.header, text='↺', font=('Aria', 16))

        # Text for preset
        self.preset_name = tk.Label(self.frame, text='Preset: Calibration Test', font=('Aria',16))

        # Text for time
        self.time_name = tk.Label(self.frame, text='Experiment Time: ', font=('Aria',16))

        # Timer for time
        """ I want to start a stopwatch-like time when the experiment play and stop buttons are
        pressed, + reset the time when a reset button is pressed
        I also want to record the current camera x,y,z coordinates during an experiment """

    def render(self):
        self.title.pack(side='left', expand=True)
        self.play_button.pack(side='left')
        self.stop_button.pack(side='left')
        self.reset_button.pack(side='left')
        self.header.pack(fill='x')
        self.preset_name.pack(anchor='w')
        self.time_name.pack(anchor='w')
        self.frame.pack(fill='both', pady=10)