""" Live microscope feed """
import tkinter as tk

class LiveFeedPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, background='white')

        # figure out live feed, no children, maybe scale bar tab

    def render(self):
        self.frame.pack(fill='both', expand=True)