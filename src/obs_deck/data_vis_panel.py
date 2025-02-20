""" Data vis tabs """
import tkinter as tk
# from obs_deck.data_vis_tabs.histogram import Histogram

class DataVisPanel:
    frame: tk.Frame
    content_frame: tk.Frame

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    def render_focus_stab(self):
        self.clear_content_frame()
        self.focus_stab.pack(fill='both', expand=True)

    def render_histogram(self):
        self.clear_content_frame()
        # self.histogram.render()

    def __init__(self, parent, store):
        # Store the store
        self.store = store
        
        # Create frame
        self.frame = tk.Label(parent)
        self.tabs = tk.Frame(self.frame)
        self.content_frame = tk.Frame(self.frame)

        # Data vis tabs
        self.focus_stab_tab = tk.Button(self.tabs, text='Focus Stabilization', font=('Aria',18), command=self.render_focus_stab)
        self.histogram_tab = tk.Button(self.tabs, text='Histogram', font=('Aria',18), command=self.render_histogram)
        self.battery_tab = tk.Button(self.tabs, text='Battery Stats', font=('Aria',18),)
        self.psf_tab = tk.Button(self.tabs, text='Point Spread Function', font=('Aria',18),)
        self.confocal_tab = tk.Button(self.tabs, text='Confocal Rendering', font=('Aria',18),)

        # Data vis renders
        self.focus_stab = tk.Label(self.content_frame, text="TBD")
        # self.histogram = Histogram(self.content_frame, store)

    def render(self):
        self.focus_stab_tab.pack(side='left', fill='x', expand=True)
        self.histogram_tab.pack(side='left', fill='x', expand=True)
        self.battery_tab.pack(side='left', fill='x', expand=True)
        self.psf_tab.pack(side='left', fill='x', expand=True)
        self.confocal_tab.pack(side='left', fill='x', expand=True)
        self.tabs.pack(fill='x')

        self.content_frame.pack(fill='both', expand=True)
        self.frame.pack(fill='both', expand=True)