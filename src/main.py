import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, master, video_source):
        self.master = master
        self.video_source = video_source
        
        # Open video source
        self.vid = cv2.VideoCapture(video_source)
        
        # Create a label for video
        self.label = tk.Label(master)
        self.label.pack()
        
        # Create control buttons
        self.create_controls()

        # Start video stream
        self.update()

    def create_controls(self):
        up_button = tk.Button(self.master, text="Up", command=lambda: self.move_camera('up'))
        up_button.pack(pady=10)

        down_button = tk.Button(self.master, text="Down", command=lambda: self.move_camera('down'))
        down_button.pack(pady=10)

        left_button = tk.Button(self.master, text="Left", command=lambda: self.move_camera('left'))
        left_button.pack(side=tk.LEFT, padx=20, pady=10)

        right_button = tk.Button(self.master, text="Right", command=lambda: self.move_camera('right'))
        right_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def move_camera(self, direction):
        print(f'Moving camera {direction}')

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to ImageTk format
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.img = img  # Keep a reference
            self.label.configure(image=img)
        self.master.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create the main window
root = tk.Tk()
root.title("Camera Control")

# Initialize the application with a video file
video_source = 'rickroll.mp4'  # Replace with your MP4 file path
app = CameraApp(root, video_source)

# Start the GUI loop
root.mainloop()
