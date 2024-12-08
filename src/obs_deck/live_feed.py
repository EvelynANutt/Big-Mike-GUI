""" Live microscope feed """
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class LiveFeedPanel:
    frame: tk.Frame

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Label(parent)

        # figure out live feed, no children, maybe scale bar tab
        self.vid = cv2.VideoCapture(1)
        self.vid_label = tk.Label(self.frame)

        self.update()

    def render(self):
        self.vid_label.pack(fill='both', expand=True)
        self.frame.pack(fill='both')

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert BGR (OpenCV) to RGB (PIL)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Dynamically resize based on the current frame dimensions
            frame_width = self.frame.winfo_width()

            if frame_width > 0:
                # Calculate the new dimensions while preserving aspect ratio
                aspect_ratio = frame.shape[1] / frame.shape[0]
                new_width = frame_width
                new_height = int(new_width / aspect_ratio)

                if new_height > 0:

                    # Resize the frame
                    resized_frame = cv2.flip(cv2.resize(frame_rgb, (new_width, new_height)), 1)

                    # Convert the resized frame to an ImageTk object
                    img = ImageTk.PhotoImage(image=Image.fromarray(resized_frame))

                    # Update the label with the new image
                    self.vid_label.img = img
                    self.vid_label.configure(image=img)

        # Call the update method again after 10ms
        self.frame.after(10, self.update)