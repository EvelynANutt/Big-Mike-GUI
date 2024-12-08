""" Data vis tabs """
import tkinter as tk

class DataVisPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent)

        # Data vis tabs
        self.tabs = tk.Frame(self.frame)
        self.spectrum_tab = tk.Button(self.tabs, text='Spectrum Graph')
        self.focus_stab_tab = tk.Button(self.tabs, text='Focus Stabilization')
        self.battery_tab = tk.Button(self.tabs, text='Battery Stats')
        self.psf_tab = tk.Button(self.tabs, text='Point Spread Function')
        self.confocal_tab = tk.Button(self.tabs, text='Confocal Rendering')

    def render(self):
        self.spectrum_tab.pack(side='left', fill='x', expand=True)
        self.focus_stab_tab.pack(side='left', fill='x', expand=True)
        self.battery_tab.pack(side='left', fill='x', expand=True)
        self.psf_tab.pack(side='left', fill='x', expand=True)
        self.confocal_tab.pack(side='left', fill='x', expand=True)
        self.tabs.pack(fill='x')
        self.frame.pack(fill='both', expand=True)