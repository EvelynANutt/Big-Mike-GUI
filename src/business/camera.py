import cv2
from threading import Thread, Event
from typing import Callable

class Camera:
    def __init__(self):
        self.vid = cv2.VideoCapture(1)
        if not self.vid.isOpened():
            print("Error: Unable to access the camera.")
        self.current_frame = None
        self.subscriptions = []
        self.running = Event()
        self.running.set()

        # Start the frame capture thread
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running.is_set():
            ret, frame = self.vid.read()
            if ret:
                self.current_frame = frame
                for subscription in self.subscriptions:
                    subscription(frame)

    def subscribe(self, callback: Callable):
        self.subscriptions.append(callback)

    def get_frame(self):
        if self.current_frame is not None:
            return self.current_frame
        else:
            raise ValueError("No frame available yet!")

    def stop(self):
        self.running.clear()
        self.thread.join()

    def __del__(self):
        self.stop()
        if self.vid.isOpened():
            self.vid.release()
