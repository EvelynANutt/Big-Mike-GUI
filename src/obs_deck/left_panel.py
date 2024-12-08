""" Active cam + experiment + quick file control """
import tkinter as tk
from obs_deck.control_panel.active_cam import ActiveCamPanel
from obs_deck.control_panel.experiment import ExperimentPanel
from obs_deck.control_panel.file import FilePanel

class LeftPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent)

        # Active cam control
        self.active_cam_panel = ActiveCamPanel(self.frame)

        # Experiment control
        self.experiment_panel = ExperimentPanel(self.frame)

        # File control
        self.file_panel = FilePanel(self.frame)


    def render(self):
        self.active_cam_panel.render()
        self.experiment_panel.render()
        self.file_panel.render()
        self.frame.pack(side='left', fill='both')