""" File control """
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image
from business.store import Store

class CapturePanel:
    frame: tk.Frame

    def picture_popup(self):
        try:
            # Convert latest frame as BGR -> RBG -> .png
            image_rgb = cv2.cvtColor(self.store.camera.get_frame(), cv2.COLOR_BGR2RGB)
            image_png = Image.fromarray(image_rgb)
            # Prompt save as window
            file_path = filedialog.asksaveasfilename(initialfile="Untitled", defaultextension='.png')
            image_png.save(file_path)
        except ValueError as e:
            print(f"Error: {e}")
    
    def play_video(self):
        # Create video
        resolution = (1920, 1080)
        codec = cv2.VideoWriter_fourcc(*"XVID")
        filename = "Recording.avi"
        # Specify frames rate
        fps = 60.0
        self.video = cv2.VideoWriter(filename, codec, fps, resolution)
        self.store.camera.subscribe(self.record)
    
    def stop_video(self):
        self.store.camera.unsubscribe(self.record)

    def record(self, frame):
        # Creating a VideoWriter object
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.video.write(frame)

    def __init__(self, parent, store: Store):
        # Store the store
        self.store = store
        
        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Capture', font=('Aria',26))

        # Take picture and take video buttons
        self.picture_button = tk.Button(self.frame, text='📷', font=('Aria',24), command=self.picture_popup)
        self.play_button = tk.Button(self.frame, text='▶', font=('Aria',24), command=None) #self.play_video)
        self.stop_button = tk.Button(self.frame, text='⏹', font=('Aria',24), command=None) #self.stop_video)
        # self.video_time_name = tk.Label(self.frame, text='Video Time: ', font=('Aria', 16))
        # self.video_timestamp = 

        """ When the picture button is pressed, I want to take a picture of the
        live video feed, then prompt the user to determine the file name and destination """
        """ When the video button is pressed, I want to prompt the user to determine
        how many photos will be taken and the time incremements for the photos,
        and prompt the user to determine the file name and destination """
        """ When the video is done being rendered, I want to notify the user """
        """ When the video is being taken, disable the picture and video buttons"""

    def render(self):
        self.title.pack(expand=True)
        self.header.pack(fill='x')
        self.picture_button.pack(side='left', fill='both', expand=True)
        self.play_button.pack(side='left', fill='both', expand=True)
        self.stop_button.pack(side='left', fill='both', expand=True)
        # self.video_time_name.pack(anchor='w')
        self.frame.pack(fill='both')