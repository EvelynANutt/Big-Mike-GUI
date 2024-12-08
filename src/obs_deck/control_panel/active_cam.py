""" Active cam control """
import tkinter as tk

class ActiveCamPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, background='blue')

        # xyz translation and xy cropping

    def render(self):
        self.frame.pack(fill='both', expand=True)