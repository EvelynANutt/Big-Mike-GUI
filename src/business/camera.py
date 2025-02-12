import cv2
from threading import Thread, Event, Lock
from typing import Callable
import PySpin
import time

# def calculate_focus_score(image,blur):
#     image_filtered=cv2.medianBlur(image,blur)
#     laplacian = cv2.Laplacian(image_filtered,cv2.CV_64F)
#     focus_score = laplacian.var()
#     return focus_score

class Camera:
    def __init__(self):
        # Initialize camera system
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()

        # Find the camera
        for i, cam in enumerate(cam_list):
            cam.Init()
        print(cam_list)
        self.cam = cam_list[0]
        self.image_result = None
        
        # Get the subscribers on
        self.subscriptions = set()
        self.lock = Lock()  # Lock for thread-safe access to subscriptions
        self.running = Event()
        self.running.set()

        # Default exp = 6000, fr = 5, gain = 0
        self.exposure = 6000
        self.frame_rate = 5
        self.gain = 0
        self.frame_time = 1.0 / self.frame_rate
        self.last_time = time.time()

        # Configure settings for camera and start streaming
        self.cam_connect_setup()
        self.configure_continuous_acquisition()
        self.cam.BeginAcquisition()

        self.cam.GetNextImage()
        print('got first image')

        # Start the frame capture thread
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()

    def cam_connect_setup(self):
        # FLIR camera setup
        #global cam
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_Mono16)
        self.cam.GainAuto.SetValue(PySpin.GainAuto_Off)
        # Set gain to 0 dB
        self.cam.Gain.SetValue(self.gain)
        self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
        # Set exposure mode to "Timed"
        self.cam.ExposureMode.SetValue(PySpin.ExposureMode_Timed)
        # Set exposure time to n microseconds
        self.cam.ExposureTime.SetValue(self.exposure)
        #self.cam.AcquisitionFrameRateEnable.SetValue(False)
        self.cam.AcquisitionFrameRate.SetValue(self.frame_rate)
    
    def update(self):
        last_time = time.time()
        print('start')
        # Retrieve the next image and run functions on current frame
        while self.running.is_set():
            self.image_result = self.cam.GetNextImage() #15000 #Timeout in milliseconds
            if self.image_result.IsIncomplete():
                # Release frame if invalid
                print(f"Image incomplete with status {self.image_result.GetImageStatus()}")
            else:
                print('got image')
                # Safely iterate through subscriptions with the lock
                with self.lock:
                    for subscription in self.subscriptions:
                        subscription(self.image_result)
            
            # Release the image
            self.image_result.Release()
            current_time = time.time()

            # Sleep for a short time before updating again
            elapsed_time = current_time - last_time
            sleep_time = max(0, self.frame_time - elapsed_time)
            time.sleep(sleep_time)  # Sleep for the remaining time if needed
            last_time = current_time       

    def subscribe(self, callback: Callable):
        with self.lock:  # Lock access to the subscriptions set
            self.subscriptions.add(callback)

    def unsubscribe(self, callback: Callable):
        with self.lock:  # Lock access to the subscriptions set
            self.subscriptions.remove(callback)

    def stop(self):
        self.running.clear()
        self.thread.join()

    def __del__(self):
        self.stop()
        try:
            self.image_result.Release()
        except:
            print('No image to release')
        cv2.destroyAllWindows()
        self.cam.EndAcquisition()
        print("Acquisition stopped.")
        self.cam.DeInit()

    def configure_continuous_acquisition(self):
        ''' Configures the camera for continuous frame acquisition and sets the buffer size to 1 frame.
        Parameters: cam (PySpin.Camera): The camera object. '''
        
        #global cam
        try:
            # Access the camera's node map
            nodemap = self.cam.GetNodeMap()

            # Set acquisition mode to Continuous
            acquisition_mode_node = PySpin.CEnumerationPtr(nodemap.GetNode("AcquisitionMode"))
            if not PySpin.IsAvailable(acquisition_mode_node) or not PySpin.IsWritable(acquisition_mode_node):
                print("AcquisitionMode node is not available or writable.")
                return False

            acquisition_mode_continuous = acquisition_mode_node.GetEntryByName("Continuous")
            if not PySpin.IsAvailable(acquisition_mode_continuous) or not PySpin.IsReadable(acquisition_mode_continuous):
                print("'Continuous' entry for AcquisitionMode is not available or readable.")
                return False

            acquisition_mode_node.SetIntValue(acquisition_mode_continuous.GetValue())
            print("Acquisition mode set to Continuous.")

            # Access the stream buffer handling mode
            stream_nodemap = self.cam.GetTLStreamNodeMap()

            # Set buffer handling mode to OldestFirst
            buffer_handling_mode_node = PySpin.CEnumerationPtr(stream_nodemap.GetNode("StreamBufferHandlingMode"))
            if not PySpin.IsAvailable(buffer_handling_mode_node) or not PySpin.IsWritable(buffer_handling_mode_node):
                print("StreamBufferHandlingMode node is not available or writable.")
                return False

            buffer_handling_mode_oldest_first = buffer_handling_mode_node.GetEntryByName("OldestFirst")
            if not PySpin.IsAvailable(buffer_handling_mode_oldest_first) or not PySpin.IsReadable(buffer_handling_mode_oldest_first):
                print("'OldestFirst' entry for StreamBufferHandlingMode is not available or readable.")
                return False

            buffer_handling_mode_node.SetIntValue(buffer_handling_mode_oldest_first.GetValue())
            print("Buffer handling mode set to OldestFirst.")

            # Set the buffer count to 1
            buffer_count_node = PySpin.CIntegerPtr(stream_nodemap.GetNode("StreamBufferCountManual"))
            if not PySpin.IsAvailable(buffer_count_node) or not PySpin.IsWritable(buffer_count_node):
                print("StreamBufferCountManual node is not available or writable.")
                return False

            buffer_count_node.SetValue(1)
            print("Buffer size set to 1 frame.")

            return True

        except PySpin.SpinnakerException as ex:
            print(f"Error: {ex}")
            return False

    def update_image2():
    #     global x_data, y_data, y_max, frame_rate, cam, x_focus, y_focus, device, step, contrast_threshold, savefigs,save_n_frames,folder, fx1,fx2,fy1,fy2, focus_stab
        
    #     # Placeholder for the OpenCV image in NiceGUI
    #     #image_placeholder = ui.image("").style("width: 500px; height: 500px;")
        
        
    #     print("Acquisition started. Press 'q' to quit.")

    #     # Track the frame rate to match the camera's frame rate
    #     frame_time = 1.0 / frame_rate  # Time between frames (in seconds)
    #     last_time = time.time()
    #     counter = 0
    #     while True:
    #         current_time = time.time()

    #         # Retrieve the next image
    #         image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

    #         if image_result.IsIncomplete():
    #             print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #             image_result.Release()
    #             continue

    #         # Convert image to a NumPy array
    #         image_data = image_result.GetNDArray()


    #         # Wait for the right amount of time to maintain the frame rate
            

    #         # Break on 'q' key press

            
    #         # Stop acquisition
            
    #     # Close OpenCV window when finished
            
    #         contrast = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)

    #         # Simulate live plot data update
    #         x_data = np.append(x_data, int(x_data[-1] + 1))
    #         y_data = np.append(y_data, contrast)

    #         if len(x_data) > 200:
    #             x_data = x_data[-200:]
    #             y_data = y_data[-200:]

    #         if contrast > y_max:
    #             y_max = contrast


    #         p_data = cv2.rectangle(np.copy(image_data), (fx1,fy1), (fx2,fy2), (2**16-1,2**16-1,2**16-1), 2)
            
    #         #cv2.imshow("Camera Feed", image_data)
    #         cv2.imshow("Camera Feed", p_data)

    #         if contrast < contrast_threshold * y_max and focus_stab == True:
    #             #try:
    #             #x_focus, y_focus, current_z = focus_scan(2000,frame_time,last_time)
                
    #             print("entering focus scan!")

    #             image_result.Release()

    #             curr_z = device.control.getPositionsAndVoltages()[2]
    #             #print('a')
    #             steps = np.linspace(curr_z-10*step,curr_z+10*step,21)
    #             #print('b')
                
                

    #             focus_score = np.array([])
    #             print('c')
    #             for i in range(len(steps)):

    #                 current_time = time.time()

    #                 device.move.setControlTargetPosition(2,steps[i])
    #                 #print('d')
    #                 time.sleep(0.16)

    #                 image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
    #                 #print('e')
    #                 if image_result.IsIncomplete():
    #                     print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                     image_result.Release()
    #                     continue

    #                 # Convert image to a NumPy array
    #                 image_data = image_result.GetNDArray()

    #                 #cv.imshow("Camera Feed", image_data)
                        
                        
    #                     #cv.axvline(500)
    #                     # Release the image
                    
    #                 fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
    #                 #print(fsc)
    #                 focus_score = np.append(focus_score,fsc)
    #                 image_result.Release()
    #                 #plt.imshow(image_data)
    #                 #plt.show()
    #                 #image_data.Release()

    #                 elapsed_time = current_time - last_time
    #                 sleep_time = max(0, frame_time - elapsed_time)
    #                 time.sleep(sleep_time)  # Sleep for the remaining time if needed



    #                 last_time = current_time

                
                
    #             print('hooray')
    #             print(focus_score)
    #             device.move.setControlTargetPosition(2,curr_z)

    #             time.sleep(0.2)


    #             o = find_peaks(focus_score,width=1.5)

    #             if len(o[0] >= 1):
    #                 peaks_temp = []
    #                 for i in o[0]:
    #                     print(i)
    #                     peaks_temp.append(focus_score[i])
    #                 mi = np.argmax(peaks_temp)
    #                 print(o[0])
    #                 print(o[1])
    #                 print(mi)

    #                 if o[1]['prominences'][mi] == max(o[1]['prominences']):

    #                     fine_target_z = steps[o[0][mi]]

    #                     device.move.setControlTargetPosition(2,fine_target_z)
    #                     image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
    #                     #print('e')
    #                     if image_result.IsIncomplete():
    #                         print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                         image_result.Release()
    #                         continue
    #                     image_result.Release()
    #                     time.sleep(0.1)

    #                     steps_final = np.linspace(fine_target_z-step*2,fine_target_z+step*2,21)

    #                     device.move.setControlTargetPosition(2,steps_final[0])

    #                     last_time = time.time()

    #                     for i in range(2):
    #                         current_time = time.time()

    #                         # Retrieve the next image
    #                         image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

    #                         if image_result.IsIncomplete():
    #                             print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                             image_result.Release()
    #                             continue

    #                         # Convert image to a NumPy array
    #                         image_data = image_result.GetNDArray()
    #                         image_result.Release()

            


    #                         # Sleep for a short time before updating again
    #                         elapsed_time = current_time - last_time
    #                         sleep_time = max(0, frame_time - elapsed_time)
    #                         time.sleep(sleep_time)  # Sleep for the remaining time if needed

    #                         last_time = current_time
                        

    #                     focus_score_final = np.array([])

    #                     for i in range(len(steps_final)):

    #                         current_time = time.time()

    #                         device.move.setControlTargetPosition(2,steps_final[i])
    #                         time.sleep(0.16)

    #                         image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

    #                         if image_result.IsIncomplete():
    #                             print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                             image_result.Release()
    #                             continue

    #                         # Convert image to a NumPy array
    #                         image_data = image_result.GetNDArray()

    #                         #cv.imshow("Camera Feed", image_data)
                                
                                
    #                             #cv.axvline(500)
    #                             # Release the image
                            
    #                         fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
    #                         #print(fsc)
    #                         focus_score_final = np.append(focus_score_final,fsc)
    #                         image_result.Release()
    #                         #plt.imshow(image_data)
    #                         #plt.show()
    #                         #image_data.Release()

    #                         elapsed_time = current_time - last_time
    #                         sleep_time = max(0, frame_time - elapsed_time)
    #                         time.sleep(sleep_time)  # Sleep for the remaining time if needed



    #                         last_time = current_time
                    
                    
                    
    #                     print(focus_score_final)
                        
    #                     fitst = np.linspace(0,20,21)

    #                     focus_score_final_filt = uniform_filter1d(focus_score_final,3)

    #                     fsff_peaks = find_peaks(focus_score_final_filt,width=1.5)
    #                     print(fsff_peaks)
    #                     if len(fsff_peaks[0]) > 1:
    #                         peaks_temp = []
    #                         for i in fsff_peaks[0]:
    #                             print(i)
    #                             peaks_temp.append(focus_score_final_filt[i])
    #                         fsff_peak = fsff_peaks[0][np.argmax(peaks_temp)]
    #                     else:
    #                         fsff_peak = fsff_peaks[0][0]


    #                     initial_guesses = [0,10, max(focus_score_final_filt),10]
    #                     print(fsff_peak)
    #                     print(initial_guesses)
    #                     if fsff_peak >= 4 and fsff_peak <= 17:
                        
    #                         params3, _ = curve_fit(NG.gauss, fitst[4:-4], focus_score_final_filt[4:-4], p0=initial_guesses)
    #                         print(params3)
    #                     elif fsff_peak < 4:
    #                         params3, _ = curve_fit(NG.gauss, fitst[:-8], focus_score_final_filt[:-8], p0=initial_guesses)
    #                         print(params3)
    #                     else:
    #                         diff = fitst - fsff_peak - 1
    #                         params3, _ = curve_fit(NG.gauss, fitst[8:], focus_score_final_filt[8:], p0=initial_guesses)
    #                         print(params3)

    #                     target_z = steps_final[0] + params3[1] * (steps_final[1]-steps_final[0])
    #                     device.move.setControlTargetPosition(2,target_z)

    #                     print('zoinks')
    #                     fig2.data[0].x = fitst
    #                     fig2.data[0].y = focus_score_final
    #                     plot_element2.update()
    #                     last_time = time.time()
    #                     for i in range(2):
    #                         current_time = time.time()

    #                         # Retrieve the next image
    #                         image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

    #                         if image_result.IsIncomplete():
    #                             print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                             image_result.Release()
    #                             continue

    #                         # Convert image to a NumPy array
    #                         image_data = image_result.GetNDArray()
    #                         image_result.Release()

            


    #                         # Sleep for a short time before updating again
    #                         elapsed_time = current_time - last_time
    #                         sleep_time = max(0, frame_time - elapsed_time)
    #                         time.sleep(sleep_time)  # Sleep for the remaining time if needed

    #                         last_time = current_time

    #                     continue  #

    #             else:

                
                
    #                 maxind = np.argmax(focus_score)
    #                 fitst = np.linspace(0,20,21)
    #                 # Initial guesses based on visual inspection 
    #                 #initial_guesses = [-5000,10,1000000]
    #                 initial_guesses = [min(focus_score),10, max(focus_score),4]

                    

    #             # Fit the parabola
    #                 params, _ = curve_fit(NG.gauss, fitst, focus_score, p0=initial_guesses)
    #                 print(params)

    #                 rough_target_z = steps[0] + params[1] * (steps[1]-steps[0])
    #                 device.move.setControlTargetPosition(2,rough_target_z)


    #                 steps_fine = steps = np.linspace(rough_target_z-10*step/5,rough_target_z+10*step/5,21)
    #                 focus_score_fine = np.array([])
    #                 #time.sleep(0.2)
    #                 for i in range(len(steps_fine)):

    #                     current_time = time.time()

    #                     device.move.setControlTargetPosition(2,steps_fine[i])
    #                     time.sleep(0.1)

    #                     image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

    #                     if image_result.IsIncomplete():
    #                         print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                         image_result.Release()
    #                         continue

    #                     # Convert image to a NumPy array
    #                     image_data = image_result.GetNDArray()

    #                     #cv.imshow("Camera Feed", image_data)
                            
                            
    #                         #cv.axvline(500)
    #                         # Release the image
                        
    #                     fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
    #                     print(fsc)
    #                     focus_score_fine = np.append(focus_score_fine,fsc)
    #                     image_result.Release()
    #                     #plt.imshow(image_data)
    #                     #plt.show()
    #                     #image_data.Release()

    #                     elapsed_time = current_time - last_time
    #                     sleep_time = max(0, frame_time - elapsed_time)
    #                     time.sleep(sleep_time)  # Sleep for the remaining time if needed



    #                     last_time = current_time

    #                 fine_target_z = steps_fine[np.argmax(focus_score_fine)]
    #                 steps_final = steps = np.linspace(fine_target_z-step/2,fine_target_z+step/2,21)
    #                 focus_score_final = np.array([])
    #                 for i in range(len(steps_final)):

    #                     current_time = time.time()

    #                     device.move.setControlTargetPosition(2,steps_final[i])
    #                     time.sleep(0.1)

    #                     image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

    #                     if image_result.IsIncomplete():
    #                         print(f"Image incomplete with status {image_result.GetImageStatus()}")
    #                         image_result.Release()
    #                         continue

    #                     # Convert image to a NumPy array
    #                     image_data = image_result.GetNDArray()

    #                     #cv.imshow("Camera Feed", image_data)
                            
                            
    #                         #cv.axvline(500)
    #                         # Release the image
                        
    #                     fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
    #                     print(fsc)
    #                     focus_score_final = np.append(focus_score_final,fsc)
    #                     image_result.Release()
    #                     #plt.imshow(image_data)
    #                     #plt.show()
    #                     #image_data.Release()

    #                     elapsed_time = current_time - last_time
    #                     sleep_time = max(0, frame_time - elapsed_time)
    #                     time.sleep(sleep_time)  # Sleep for the remaining time if needed



    #                     last_time = current_time


    #                 #coefficients = np.polyfit(fitst,focus_score,2)
    #                 params2, _ = curve_fit(NG.gauss, fitst, focus_score_fine, p0=initial_guesses)
    #                 print(params2)

    #                 params3, _ = curve_fit(NG.gauss, fitst, focus_score_final, p0=initial_guesses)
    #                 print(params3)



    #                 target_z = steps_final[0] + params3[1] * (steps_final[1]-steps_final[0])
    #                 device.move.setControlTargetPosition(2,target_z)


    #                 print('zoinks')
    #                 fig2.data[0].x = fitst
    #                 fig2.data[0].y = focus_score_final
    #                 plot_element2.update()
    #                 continue  #
    #             #except:
    #                 #cam.EndAcquisition()
    #                 #cam.DeInit()
                
                
    #             #fsdata = focus_scan(2000,frame_time,last_time)
    #             #fig2.update_layout(shapes=[dict(type='line', y0=y_max, y1=y_max, x0=0, x1=1, xref='paper', yref='y')])
            

    #             # Update the plot with new data
            

                

    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

            
    #         fig.update_layout(shapes=[dict(type='line', y0=y_max, y1=y_max, x0=0, x1=1, xref='paper', yref='y')])
            

    #         # Update the plot with new data
    #         fig.data[0].x = x_data
    #         fig.data[0].y = y_data
    #         plot_element.update()  # This correctly triggers the update of the Plotly plot

    #         if savefigs == True and counter % save_n_frames == 0:
    #             savetime = np.round(time.time(),2)
    #             filename = folder + str(counter) + '-' + str(savetime).split('.')[0] + 'p' + str(savetime).split('.')[1] +  '.pgm'
    #             cv2.imwrite(filename,image_data)
            
            
    #         image_result.Release()

            
    #         counter += 1

    #         # Sleep for a short time before updating again
    #         elapsed_time = current_time - last_time
    #         sleep_time = max(0, frame_time - elapsed_time)
    #         time.sleep(sleep_time)  # Sleep for the remaining time if needed

    #         last_time = current_time
    #     try:
    #         image_result.Release()
    #     except:
    #         print('No image to release')
    #     cv2.destroyAllWindows()
    #     cam.EndAcquisition()
    #     print("Acquisition stopped.")
    #     cam.DeInit()
            print(1+1)
