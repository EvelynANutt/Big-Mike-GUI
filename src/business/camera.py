import cv2
from threading import Thread, Event, Lock
from typing import Callable
import PySpin
import queue
import time

# def calculate_focus_score(image,blur):
#     image_filtered=cv2.medianBlur(image,blur)
#     laplacian = cv2.Laplacian(image_filtered,cv2.CV_64F)
#     focus_score = laplacian.var()
#     return focus_score

class Camera:
    def __init__(self):
        # Get the subscribers on
        self.subscriptions = set()
        self.lock = Lock()  # Lock for thread-safe access to subscriptions
        self.running = Event()
        self.running.set()

        self.frame = None

        # Default exp = 6000, fr = 5, gain = 0
        self.exposure = 6000
        self.frame_rate = 5
        self.gain = 0

        self.frame_queue = queue.Queue()

        # Start the frame capture thread
        self.thread = Thread(target=self.run_thread, daemon=True)
        self.thread.start()

    def get_frame(self):
        with self.lock:
            return self.frame

    def cam_connect_setup(self):
        time.sleep(1)
        # FLIR camera setup
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_Mono16)
        self.cam.GainAuto.SetValue(PySpin.GainAuto_Off)
        # Set gain to 0 dB
        self.cam.Gain.SetValue(self.gain)
        self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
        # Set exposure mode to "Timed"
        self.cam.ExposureMode.SetValue(PySpin.ExposureMode_Timed)
        # Set exposure time to n microseconds
        self.cam.ExposureTime.SetValue(self.exposure)
        # self.cam.AcquisitionFrameRateEnable.SetValue(False)
        # time.sleep(1)
        # self.cam.AcquisitionFrameRate.SetValue(self.frame_rate)
    
    def run_thread(self):
        # Initialize camera system
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()
        
        if cam_list.GetSize() == 0:
            print("No camera found!")
            system.ReleaseInstance()
            return
        else:
            print(f"Found {cam_list.GetSize()} camera(s)")

        self.cam = cam_list.GetByIndex(0)
        if self.cam.IsInitialized():
            print("DEINIT")
            self.cam.DeInit()
        self.cam.Init()

        try:
            # Configure settings for camera and start streaming
            self.cam_connect_setup()
            self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
            self.cam.BeginAcquisition()

            # Retrieve the next image and run functions on current frame
            while self.running.is_set():
                image_result = self.cam.GetNextImage(1000) #15000 #Timeout in milliseconds
                if image_result.IsIncomplete():
                    # Release frame if invalid
                    print(f"Image incomplete with status {image_result.GetImageStatus()}")
                    image_result.Release()
                else:
                    image_data = image_result.GetNDArray()
                    image_result.Release()
                    image_rgb = cv2.cvtColor(image_data, cv2.COLOR_BAYER_BG2RGB)

                    # Safely iterate through subscriptions with the lock
                    with self.lock:
                        self.frame = image_rgb
                        for subscription in self.subscriptions:
                            subscription(image_rgb)
        finally:
            self.cam.EndAcquisition()
            self.cam.DeInit()
            del self.cam
            cam_list.Clear()
            system.ReleaseInstance()

    def subscribe(self, callback: Callable):
        with self.lock:  # Lock access to the subscriptions set
            self.subscriptions.add(callback)

    def unsubscribe(self, callback: Callable):
        with self.lock:  # Lock access to the subscriptions set
            self.subscriptions.remove(callback)

    def set_exposure_value(self, new_value: float):
        self.cam.ExposureTime.SetValue(new_value)
        # print("Recieved: ", self.cam.GetExposureTime())
        self.exposure = new_value

    # def set_frame_rate_value(self, new_value: float):
    #     self.cam.AcquisitionFrameRate.SetValue(new_value)
    #     self.frame_rate = new_value

    def set_gain_value(self, new_value: float):
        self.cam.Gain.SetValue(new_value)
        self.gain = new_value

    def stop(self):
        self.running.clear()
        self.thread.join()

    def __del__(self):
        self.stop()
        cv2.destroyAllWindows()

# if __name__ == "__main__":
#     import time
#     app = Camera()
#     time.sleep(10)
