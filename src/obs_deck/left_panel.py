""" Stage + experiment + quick file control """
import tkinter as tk
from obs_deck.control_panel.stage_controls import StageControlPanel
from obs_deck.control_panel.capture import CapturePanel
from obs_deck.control_panel.cam_settings import CameraSettingsPanel
# from obs_deck.control_panel.experiment import ExperimentPanel

class LeftPanel:
    frame: tk.Frame

    def __init__(self, parent, store):
        # Store the store
        self.store = store

        # Create frame
        self.frame = tk.Label(parent)

        # Stage control
        self.stage_control_panel = StageControlPanel(self.frame, store)

        # File control
        self.capture_panel = CapturePanel(self.frame, store)

        # Camera settings
        self.camera_settings_panel = CameraSettingsPanel(self.frame, store)

        # Experiment control
        # self.experiment_panel = ExperimentPanel(self.frame, store)


    def render(self):
        self.stage_control_panel.render()
        self.capture_panel.render()
        self.camera_settings_panel.render()
        # self.experiment_panel.render()
        self.frame.pack(side='left', fill='both')