""" File control """
import tkinter as tk

class CapturePanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Capture', font=('Aria',26))

        # Take picture and take video buttons
        self.picture_button = tk.Button(self.frame, text='Take Picture', font=('Aria',20))
        self.video_button = tk.Button(self.frame, text='Take Video', font=('Aria',20))

    def render(self):
        self.title.pack(expand=True)
        self.header.pack(fill='x')
        self.picture_button.pack(fill='x')
        self.video_button.pack(fill='x')
        self.frame.pack(fill='both')