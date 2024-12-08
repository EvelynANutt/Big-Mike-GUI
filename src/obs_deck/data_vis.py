""" Data vis tabs """
import tkinter as tk

class DataVisPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, background='purple')

        # Data vis tabs

    def render(self):
        self.frame.pack(fill='both', expand=True)