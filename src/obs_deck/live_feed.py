""" Live microscope feed """
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from business.store import Store

class LiveFeedPanel:
    frame: tk.Frame

    def __init__(self, parent, store: Store):
        # Store the store
        self.store = store
        
        # Create frame
        self.frame = tk.Label(parent)
        self.vid_label = tk.Label(self.frame)

        self.update()

    def update(self):
        self.display_camera()
        self.frame.after(10, self.update)

    def display_camera(self):
        camera_frame = self.store.camera.get_frame()
        if camera_frame is None:
            return

        # Dynamically resize based on the current frame dimensions
        frame_width = self.frame.winfo_width()

        if frame_width > 0:
            # Calculate the new dimensions while preserving aspect ratio
            aspect_ratio = camera_frame.shape[1] / camera_frame.shape[0]
            new_width = frame_width
            new_height = int(new_width / aspect_ratio)

            # Cap the height to 400 pixels
            if new_height > 400:
                new_height = 400
                new_width = int(new_height * aspect_ratio)

            if new_height > 0:
                # Resize the frame
                resized_frame = cv2.flip(cv2.resize(camera_frame, (new_width, new_height)), 1)

                # Convert the resized frame to an ImageTk object
                img = ImageTk.PhotoImage(image=Image.fromarray(resized_frame))

                # Update the label with the new image
                self.vid_label.img = img
                self.vid_label.configure(image=img)

    """ At some point here, I want to enable some cropping stuff, 
    but it's not entirely urgent """
   
    def render(self):
        self.vid_label.pack(fill='both', expand=True)
        self.frame.pack(fill='both')
