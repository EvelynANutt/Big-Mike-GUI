import cv2
from threading import Thread, Event, Lock
from typing import Callable

class Camera:
    def __init__(self):
        self.vid = cv2.VideoCapture(1)
        if not self.vid.isOpened():
            print("Error: Unable to access the camera.")
        self.current_frame = None
        self.subscriptions = set()
        self.lock = Lock()  # Lock for thread-safe access to subscriptions
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
                # Safely iterate through subscriptions with the lock
                with self.lock:
                    for subscription in self.subscriptions:
                        subscription(frame)

    def subscribe(self, callback: Callable):
        with self.lock:  # Lock access to the subscriptions set
            self.subscriptions.add(callback)

    def unsubscribe(self, callback: Callable):
        with self.lock:  # Lock access to the subscriptions set
            self.subscriptions.remove(callback)

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
