import os
#os.environ["OMP_NUM_THREADS"] = "1"
#os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
import io
import base64
from nicegui import ui
import threading
import time
import plotly.graph_objs as go
from PIL import Image as PILImage
from io import BytesIO
import PySpin
import sys
sys.path.append("./")
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter1d

# Contrast for focus stab:
contrast_threshold = 0.7

#2000 works well for 10x. 200 for 100x,300 was used for 40x - will use 750 for 20x
step=1000 # distance to look for max contrast
z_lim= 25000 # if we move too far, turn autofocus off

#these variables are for the xy positions of the upper left corner and lower right corner
fx1,fy1,fx2,fy2 = 540,120,650,200 # rectangle for autofocusing region, turn into draggable rectangle
focus_stab = True


def update_image2():
    global x_data, y_data, y_max, frame_rate, cam, x_focus, y_focus, device, step, contrast_threshold, savefigs,save_n_frames,folder, fx1,fx2,fy1,fy2, focus_stab,z_lim
    
    # Placeholder for the OpenCV image in NiceGUI
    #image_placeholder = ui.image("").style("width: 500px; height: 500px;")
    
    
    print("Acquisition started. Press 'q' to quit.")

    # Track the frame rate to match the camera's frame rate
    
    counter = 0
    while True:
        
        contrast = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)

        # Simulate live plot data update
        x_data = np.append(x_data, int(x_data[-1] + 1))
        y_data = np.append(y_data, contrast)

        if len(x_data) > 200:
            x_data = x_data[-200:]
            y_data = y_data[-200:]

        if contrast > y_max:
            y_max = contrast

        # Draw rectangle of focus area over live feed in GUI
        p_data = cv2.rectangle(np.copy(image_data), (fx1,fy1), (fx2,fy2), (2**16-1,2**16-1,2**16-1), 2)
        p_data_r =cv2.resize(p_data, (1152,720)) # Resizing Nice GUI window
        #cv2.imshow("Camera Feed", image_data)
        cv2.imshow("Camera Feed", p_data)

        # Decide when to make focus_stab == True after it becomes false
        if contrast < contrast_threshold * y_max and focus_stab == True:
            
            print("entering focus scan!")
            image_result.Release()

            curr_z = device.control.getPositionsAndVoltages()[2]
            steps = np.linspace(curr_z-10*step,curr_z+10*step,21) # Defining range to sample contrast

            # Keep track of focus scores
            focus_score = np.array([])

            # Loop over all the steps so we can calculate focus scores
            for i in range(len(steps)):

                current_time = time.time()

                # Move to new z position
                device.move.setControlTargetPosition(2,steps[i])
                time.sleep(0.16)

                image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
                if image_result.IsIncomplete():
                    print(f"Image incomplete with status {image_result.GetImageStatus()}")
                    image_result.Release()
                    continue
                # Convert image to a NumPy array
                image_data = image_result.GetNDArray()

                # Take the image and calculate focus score
                fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
                #print(fsc)

                # Add to focus score record
                focus_score = np.append(focus_score,fsc)
                image_result.Release()
                # Buffer tracking
                elapsed_time = current_time - last_time
                sleep_time = max(0, frame_time - elapsed_time)
                time.sleep(sleep_time)  # Sleep for the remaining time if needed
                last_time = current_time

            # Now we have all focus scores for 20 steps in z
            print('hooray')
            print(focus_score)
            # Go back to where we started
            device.move.setControlTargetPosition(2,curr_z)
            time.sleep(0.2)

            # Start finding max of the focus scores we got
            o = find_peaks(focus_score,width=1.5)

            if len(o[0] >= 1):
                peaks_temp = []
                # o[0] is the positions of the peaks
                for i in o[0]:
                    print(i)
                    peaks_temp.append(focus_score[i])
                # Find peak with max focus score
                mi = np.argmax(peaks_temp)
                print(o[0])
                print(o[1])
                print(mi)

                # if peak with max focus score is also the most prominent peak
                if o[1]['prominences'][mi] == max(o[1]['prominences']):
                    
                    # Define new finer target for sampling over smaller steps
                    fine_target_z = steps[o[0][mi]]
                    # Go to that peak for new distribution
                    device.move.setControlTargetPosition(2,fine_target_z)
                    image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
                    if image_result.IsIncomplete():
                        print(f"Image incomplete with status {image_result.GetImageStatus()}")
                        image_result.Release()
                        continue
                    image_result.Release()
                    time.sleep(0.1)

                    # Define steps of finer distribution
                    steps_final = np.linspace(fine_target_z-step*2,fine_target_z+step*2,21)
                    # Move to the beginning of the distribution
                    device.move.setControlTargetPosition(2,steps_final[0])

                    # Buffer stuff
                    last_time = time.time()
                    for i in range(2):
                        current_time = time.time()
                        # Retrieve the next image
                        image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds
                        if image_result.IsIncomplete():
                            print(f"Image incomplete with status {image_result.GetImageStatus()}")
                            image_result.Release()
                            continue
                        # Convert image to a NumPy array
                        image_data = image_result.GetNDArray()
                        image_result.Release()
                        # Sleep for a short time before updating again
                        elapsed_time = current_time - last_time
                        sleep_time = max(0, frame_time - elapsed_time)
                        time.sleep(sleep_time)  # Sleep for the remaining time if needed
                        last_time = current_time
                    
                    # Record for the finer distribution focus scores
                    focus_score_final = np.array([])

                    # Get focus scores for finer distribution
                    for i in range(len(steps_final)):
                        current_time = time.time()
                        device.move.setControlTargetPosition(2,steps_final[i])
                        time.sleep(0.16)

                        image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds
                        if image_result.IsIncomplete():
                            print(f"Image incomplete with status {image_result.GetImageStatus()}")
                            image_result.Release()
                            continue

                        # Convert image to a NumPy array
                        image_data = image_result.GetNDArray()
                        
                        # Calculate focus score
                        fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
                        #print(fsc)

                        # Add focus score to finer distribution record
                        focus_score_final = np.append(focus_score_final,fsc)
                        image_result.Release()

                        elapsed_time = current_time - last_time
                        sleep_time = max(0, frame_time - elapsed_time)
                        time.sleep(sleep_time)  # Sleep for the remaining time if needed
                        last_time = current_time
                
                    # Now we have record of finer distribution focus scores
                    print(focus_score_final)
                    
                    # Steps for fitting & plotting the Gaussian
                    fitst = np.linspace(0,20,21)

                    # Make the finer distribution into a more uniform Gaussian
                    focus_score_final_filt = uniform_filter1d(focus_score_final,3)

                    # Find peaks of that uniform Gaussian
                    fsff_peaks = find_peaks(focus_score_final_filt,width=1.5)
                    print(fsff_peaks)
                    if len(fsff_peaks[0]) > 1:
                        peaks_temp = []
                        for i in fsff_peaks[0]:
                            print(i)
                            peaks_temp.append(focus_score_final_filt[i])
                        # Find the peak with the greatest focus score
                        fsff_peak = fsff_peaks[0][np.argmax(peaks_temp)]
                    else:
                        fsff_peak = fsff_peaks[0][0]

                    # Fit Gaussian to position of max focus score found with initial parameters of Gaussian to give to fitting function
                    initial_guesses = [0,10, max(focus_score_final_filt),10]
                    print(fsff_peak)
                    print(initial_guesses)
                    # Define overall distribution as an accurate Gaussian
                    if fsff_peak >= 4 and fsff_peak <= 17:
                        params3, _ = curve_fit(NG.gauss, fitst[4:-4], focus_score_final_filt[4:-4], p0=initial_guesses)
                        print(params3)
                    elif fsff_peak < 4:
                        params3, _ = curve_fit(NG.gauss, fitst[:-8], focus_score_final_filt[:-8], p0=initial_guesses)
                        print(params3)
                    else:
                        diff = fitst - fsff_peak - 1
                        params3, _ = curve_fit(NG.gauss, fitst[8:], focus_score_final_filt[8:], p0=initial_guesses)
                        print(params3)
                    
                    # Position of peak z overall in nm
                    target_z = steps_final[0] + params3[1] * (steps_final[1]-steps_final[0])
                    # Move there!
                    device.move.setControlTargetPosition(2,target_z)

                    # Don't go too far out of range
                    if abs(target_z) > z_lim:
                        focus_stab=False 

                    # Do the plotting here!!!

                    for i in range(2):
                        current_time = time.time()
                        # Retrieve the next image
                        image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds
                        if image_result.IsIncomplete():
                            print(f"Image incomplete with status {image_result.GetImageStatus()}")
                            image_result.Release()
                            continue
                        # Convert image to a NumPy array
                        image_data = image_result.GetNDArray()
                        image_result.Release()
                        # Sleep for a short time before updating again
                        elapsed_time = current_time - last_time
                        sleep_time = max(0, frame_time - elapsed_time)
                        time.sleep(sleep_time)  # Sleep for the remaining time if needed
                        last_time = current_time
        counter += 1
        continue
    
