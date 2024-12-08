""" Top header """
import tkinter as tk
from PIL import ImageTk, Image

class Header:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Frame(parent)

        # Logo label
        logo_img = Image.open('/Users/evelynanutt/GitHub/Big-Mike-GUI/src/bigmike_logo.png')
        self.logo_img = ImageTk.PhotoImage(logo_img.resize((100,100)))
        self.logo = tk.Label(self.frame, image=self.logo_img)

        # Tabs label
        self.tabs = tk.Label(self.frame, background='red')

    def render(self):
        self.logo.pack(side='left')
        self.tabs.pack(side='left', fill='both', expand=True)
        self.frame.pack(fill='both')
