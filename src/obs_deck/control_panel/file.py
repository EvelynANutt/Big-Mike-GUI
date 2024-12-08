""" File control """
import tkinter as tk

class FilePanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, background='pink')

        # Take picture and take video buttons

    def render(self):
        self.frame.pack(fill='both', expand=True)