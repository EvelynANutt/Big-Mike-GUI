""" Data vis tabs """
import tkinter as tk
from obs_deck.data_vis_tabs.histogram import Histogram

class DataVisPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent)

        # Data vis tabs
        self.tabs = tk.Frame(self.frame)
        self.histogram_tab = tk.Button(self.tabs, text='Histogram')
        self.focus_stab_tab = tk.Button(self.tabs, text='Focus Stabilization')
        self.battery_tab = tk.Button(self.tabs, text='Battery Stats')
        self.psf_tab = tk.Button(self.tabs, text='Point Spread Function')
        self.confocal_tab = tk.Button(self.tabs, text='Confocal Rendering')
        self.histogram = Histogram(self.frame)

    def render(self):
        self.histogram_tab.pack(side='left', fill='x', expand=True)
        self.focus_stab_tab.pack(side='left', fill='x', expand=True)
        self.battery_tab.pack(side='left', fill='x', expand=True)
        self.psf_tab.pack(side='left', fill='x', expand=True)
        self.confocal_tab.pack(side='left', fill='x', expand=True)
        self.tabs.pack(fill='x')
        self.histogram.render()
        self.frame.pack(fill='both', expand=True)