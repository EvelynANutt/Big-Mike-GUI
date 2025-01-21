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
        self.tabs = tk.Frame(self.frame)
        self.obs_deck_tab = tk.Button(self.tabs, text='Observation Deck')
        self.cam_setting_tab = tk.Button(self.tabs, text='Camera Settings')
        self.experiment_setup_tab = tk.Button(self.tabs, text='Experiment Setup')
        self.system_properties_tab = tk.Button(self.tabs, text='System Properties')
        self.post_processing_tab = tk.Button(self.tabs, text='Post-Processing')
        
    def render(self):
        self.logo.pack(side='left')
        self.obs_deck_tab.pack(side='left', fill='both', expand=True)
        self.cam_setting_tab.pack(side='left', fill='both', expand=True)
        self.experiment_setup_tab.pack(side='left', fill='both', expand=True)
        self.system_properties_tab.pack(side='left', fill='both', expand=True)
        self.post_processing_tab.pack(side='left', fill='both', expand=True)
        self.tabs.pack(side='left', fill='both', expand=True)
        self.frame.pack(fill='both')
