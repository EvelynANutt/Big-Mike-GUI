""" Stage + experiment + quick file control """
import tkinter as tk
from obs_deck.control_panel.stage_controls import StageControlPanel
from obs_deck.control_panel.capture import CapturePanel
from obs_deck.control_panel.cam_settings import CameraSettingsPanel
# from obs_deck.control_panel.experiment import ExperimentPanel

class LeftPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent)

        # Stage control
        self.stage_control_panel = StageControlPanel(self.frame)

        # File control
        self.capture_panel = CapturePanel(self.frame)

        # Camera settings
        self.camera_settings_panel = CameraSettingsPanel(self.frame)

        # Experiment control
        # self.experiment_panel = ExperimentPanel(self.frame)


    def render(self):
        self.stage_control_panel.render()
        self.capture_panel.render()
        self.camera_settings_panel.render()
        # self.experiment_panel.render()
        self.frame.pack(side='left', fill='both')