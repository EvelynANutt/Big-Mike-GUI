""" Stage control """
import tkinter as tk
from obs_deck.control_panel.stage_control_input import StageControlInput
from business.store import Store

class StageControlPanel:
    frame: tk.Frame

    def __init__(self, parent, store: Store):
        # Store the store
        self.store = store

        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Stage Controls', font=('Aria',26))

        # xyz translation and xy cropping names
        self.x_trans_input = StageControlInput(self.frame, self.store, dim=0)
        self.y_trans_input = StageControlInput(self.frame, self.store, dim=1)
        self.z_trans_input = StageControlInput(self.frame, self.store, dim=2)

    def render(self):
        self.title.pack(side='left', expand=True)
        self.header.pack(fill='x')
        self.x_trans_input.render()
        self.y_trans_input.render()
        self.z_trans_input.render()
        self.frame.pack(fill='both')