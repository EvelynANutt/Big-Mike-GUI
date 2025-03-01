# live microscope feed & data vis
import tkinter as tk
from obs_deck.live_feed import LiveFeedPanel
from obs_deck.data_vis import DataVisPanel

class RightPanel:
    frame: tk.Frame

    def __init__(self, parent, store):
        # Store the store
        self.store = store

        # Create frame
        self.frame = tk.Label(parent)

        # Live feed panel
        self.live_feed_panel = LiveFeedPanel(self.frame, store)

        # Data vis panel
        self.data_vis_panel = DataVisPanel(self.frame, store)

    def render(self):
        self.live_feed_panel.render()
        self.data_vis_panel.render()
        self.frame.pack(side='left', fill='both', expand=True)