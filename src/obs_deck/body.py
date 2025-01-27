""" Main section of UI """
import tkinter as tk
from obs_deck.left_panel import LeftPanel
from obs_deck.right_panel import RightPanel

class Body:
    frame: tk.Frame

    def __init__(self, parent, store):
        # Store the store
        self.store = store

        # Create frame
        self.frame = tk.Frame(parent)

        # Right panel 
        self.right_panel = RightPanel(self.frame, self.store)

        # Left panel 
        self.left_panel = LeftPanel(self.frame, self.store)

    def render(self):
        self.left_panel.render()
        self.right_panel.render()
        self.frame.pack(fill='both', expand=True)
