""" Experiment control """
import tkinter as tk

class ExperimentPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, background='black')

        # Text for preset and play/stop buttons

    def render(self):
        self.frame.pack(fill='both', expand=True)