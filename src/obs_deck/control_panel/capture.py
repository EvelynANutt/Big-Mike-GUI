""" File control """
import tkinter as tk

class CapturePanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Capture', font=('Aria',26))

        # Take picture and take video buttons
        self.picture_button = tk.Button(self.frame, text='Take Picture', font=('Aria',20))
        self.video_button = tk.Button(self.frame, text='Take Video', font=('Aria',20))
        # self.video_time_name = tk.Label(self.frame, text='Video Time: ', font=('Aria', 16))
        # self.video_timestamp = 
        """ When the picture button is pressed, I want to take a picture of the
        live video feed, then prompt the user to determine the file name and destination """
        """ When the video button is pressed, I want to prompt the user to determine
        how many photos will be taken and the time incremements for the photos,
        and prompt the user to determine the file name and destination """
        """ When the video is done being rendered, I want to notify the user """

    def render(self):
        self.title.pack(expand=True)
        self.header.pack(fill='x')
        self.picture_button.pack(fill='x')
        self.video_button.pack(fill='x')
        # self.video_time_name.pack(anchor='w')
        self.frame.pack(fill='both')