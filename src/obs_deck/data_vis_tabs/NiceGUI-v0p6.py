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
import AMC
import NiceGUIfunctions as NG
device=AMC.Device('192.168.1.1')
device.connect()



# Initial data for the plot
x_data = np.array([0])
y_data = np.array([0])
focus_x = np.array([0])
focus_y = np.array([0])
y_max = 0
frame_rate = 5
contrast_threshold = 0.7
#2000 works well for 10x. 200 for 100x,300 was used for 40x - will use 750 for 20x
step=1000
savefigs = True
save_n_frames = 25
folder = "C:/Users/bigmi/OneDrive/Desktop/Kyle/20250213-PC1836/AutofocusExpt-Continued6/"
z_lim= 25000

#these variables are for the xy positions of the upper left corner and lower right corner
fx1,fy1,fx2,fy2 = 540,120,650,200
focus_stab = True




system = PySpin.System.GetInstance()
cam_list = system.GetCameras()
num_Cameras = cam_list.GetSize()

for i, cam in enumerate(cam_list):
    cam.Init()
print(cam_list)

cam = cam_list[0]






NG.cam_connect_setup(cam)
NG.configure_continuous_acquisition(cam)
cam.BeginAcquisition()
current_z = device.control.getPositionsAndVoltages()[2]
# Create a figure using Plotly
fig = go.Figure(
    data=[go.Scatter(x=x_data, y=y_data, mode='lines', name='Sine Wave')],
    layout=go.Layout(
        title='Live Updating Plot',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Amplitude'),
    )
)

fig.add_shape(type='line',
                x0=0,
                y0=y_max,
                x1=1,
                y1=y_max,
                line=dict(color='Red',),
                xref='paper',
                yref='y'
)

fig2 = go.Figure(
    data=[go.Scatter(x=focus_x, y=focus_y, mode='lines', name='Sine Wave')],
    layout=go.Layout(
        title='Live Updating Plot',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Amplitude'),
    )
)

fig2.add_shape(type='line',
                x0=0,
                y0=y_max,
                x1=1,
                y1=y_max,
                line=dict(color='Red',),
                xref='paper',
                yref='y'
)

# Create a plotly figure to display in NiceGUI
plot_element = ui.plotly(fig)
plot_element2 = ui.plotly(fig2)

# Function to generate random image (simulating a video feed)



def update_image2():
    global x_data, y_data, y_max, frame_rate, cam, x_focus, y_focus, device, step, contrast_threshold, savefigs,save_n_frames,folder, fx1,fx2,fy1,fy2, focus_stab,z_lim
    
    # Placeholder for the OpenCV image in NiceGUI
    #image_placeholder = ui.image("").style("width: 500px; height: 500px;")
    
    
    print("Acquisition started. Press 'q' to quit.")

    # Track the frame rate to match the camera's frame rate
    frame_time = 1.0 / frame_rate  # Time between frames (in seconds)
    last_time = time.time()
    counter = 0
    while True:
        current_time = time.time()

        # Retrieve the next image
        image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

        if image_result.IsIncomplete():
            print(f"Image incomplete with status {image_result.GetImageStatus()}")
            image_result.Release()
            continue

        # Convert image to a NumPy array
        image_data = image_result.GetNDArray()


        # Wait for the right amount of time to maintain the frame rate
        

        # Break on 'q' key press

        
        # Stop acquisition
        
    # Close OpenCV window when finished
        
        contrast = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)

        # Simulate live plot data update
        x_data = np.append(x_data, int(x_data[-1] + 1))
        y_data = np.append(y_data, contrast)

        if len(x_data) > 200:
            x_data = x_data[-200:]
            y_data = y_data[-200:]

        if contrast > y_max:
            y_max = contrast


        p_data = cv2.rectangle(np.copy(image_data), (fx1,fy1), (fx2,fy2), (2**16-1,2**16-1,2**16-1), 2)
        
        p_data_r =cv2.resize(p_data, (1152,720))

        #cv2.imshow("Camera Feed", image_data)
        cv2.imshow("Camera Feed", p_data)

        if contrast < contrast_threshold * y_max and focus_stab == True:
            #try:
            #x_focus, y_focus, current_z = focus_scan(2000,frame_time,last_time)
            
            print("entering focus scan!")

            image_result.Release()

            curr_z = device.control.getPositionsAndVoltages()[2]
            #print('a')
            steps = np.linspace(curr_z-10*step,curr_z+10*step,21)
            #print('b')
            
            

            focus_score = np.array([])
            print('c')
            for i in range(len(steps)):

                current_time = time.time()

                device.move.setControlTargetPosition(2,steps[i])
                #print('d')
                time.sleep(0.16)

                image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
                #print('e')
                if image_result.IsIncomplete():
                    print(f"Image incomplete with status {image_result.GetImageStatus()}")
                    image_result.Release()
                    continue

                # Convert image to a NumPy array
                image_data = image_result.GetNDArray()

                #cv.imshow("Camera Feed", image_data)
                    
                    
                    #cv.axvline(500)
                    # Release the image
                
                fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
                #print(fsc)
                focus_score = np.append(focus_score,fsc)
                image_result.Release()
                #plt.imshow(image_data)
                #plt.show()
                #image_data.Release()

                elapsed_time = current_time - last_time
                sleep_time = max(0, frame_time - elapsed_time)
                time.sleep(sleep_time)  # Sleep for the remaining time if needed



                last_time = current_time

            
            
            print('hooray')
            print(focus_score)
            device.move.setControlTargetPosition(2,curr_z)

            time.sleep(0.2)


            o = find_peaks(focus_score,width=1.5)

            if len(o[0] >= 1):
                peaks_temp = []
                for i in o[0]:
                    print(i)
                    peaks_temp.append(focus_score[i])
                mi = np.argmax(peaks_temp)
                print(o[0])
                print(o[1])
                print(mi)

                if o[1]['prominences'][mi] == max(o[1]['prominences']):

                    fine_target_z = steps[o[0][mi]]

                    device.move.setControlTargetPosition(2,fine_target_z)
                    image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
                    #print('e')
                    if image_result.IsIncomplete():
                        print(f"Image incomplete with status {image_result.GetImageStatus()}")
                        image_result.Release()
                        continue
                    image_result.Release()
                    time.sleep(0.1)

                    steps_final = np.linspace(fine_target_z-step*2,fine_target_z+step*2,21)

                    device.move.setControlTargetPosition(2,steps_final[0])

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
                    

                    focus_score_final = np.array([])

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

                        #cv.imshow("Camera Feed", image_data)
                            
                            
                            #cv.axvline(500)
                            # Release the image
                        
                        fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
                        #print(fsc)
                        focus_score_final = np.append(focus_score_final,fsc)
                        image_result.Release()
                        #plt.imshow(image_data)
                        #plt.show()
                        #image_data.Release()

                        elapsed_time = current_time - last_time
                        sleep_time = max(0, frame_time - elapsed_time)
                        time.sleep(sleep_time)  # Sleep for the remaining time if needed



                        last_time = current_time
                
                
                
                    print(focus_score_final)
                    
                    fitst = np.linspace(0,20,21)

                    focus_score_final_filt = uniform_filter1d(focus_score_final,3)

                    fsff_peaks = find_peaks(focus_score_final_filt,width=1.5)
                    print(fsff_peaks)
                    if len(fsff_peaks[0]) > 1:
                        peaks_temp = []
                        for i in fsff_peaks[0]:
                            print(i)
                            peaks_temp.append(focus_score_final_filt[i])
                        fsff_peak = fsff_peaks[0][np.argmax(peaks_temp)]
                    else:
                        fsff_peak = fsff_peaks[0][0]


                    initial_guesses = [0,10, max(focus_score_final_filt),10]
                    print(fsff_peak)
                    print(initial_guesses)
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

                    target_z = steps_final[0] + params3[1] * (steps_final[1]-steps_final[0])
                    device.move.setControlTargetPosition(2,target_z)

                    if abs(target_z) > z_lim:
                        focus_stab=False 

                    print('zoinks')
                    fig2.data[0].x = fitst
                    fig2.data[0].y = focus_score_final
                    plot_element2.update()
                    last_time = time.time()
                    y_max = max(focus_score_final_filt)
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

                    continue  #

            else:

            
            
                maxind = np.argmax(focus_score)
                fitst = np.linspace(0,20,21)
                # Initial guesses based on visual inspection 
                #initial_guesses = [-5000,10,1000000]
                initial_guesses = [min(focus_score),10, max(focus_score),4]

                

            # Fit the parabola
                params, _ = curve_fit(NG.gauss, fitst, focus_score, p0=initial_guesses)
                print(params)

                rough_target_z = steps[0] + params[1] * (steps[1]-steps[0])
                device.move.setControlTargetPosition(2,rough_target_z)


                steps_fine = steps = np.linspace(rough_target_z-10*step/5,rough_target_z+10*step/5,21)
                focus_score_fine = np.array([])
                #time.sleep(0.2)
                for i in range(len(steps_fine)):

                    current_time = time.time()

                    device.move.setControlTargetPosition(2,steps_fine[i])
                    time.sleep(0.1)

                    image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

                    if image_result.IsIncomplete():
                        print(f"Image incomplete with status {image_result.GetImageStatus()}")
                        image_result.Release()
                        continue

                    # Convert image to a NumPy array
                    image_data = image_result.GetNDArray()

                    #cv.imshow("Camera Feed", image_data)
                        
                        
                        #cv.axvline(500)
                        # Release the image
                    
                    fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
                    print(fsc)
                    focus_score_fine = np.append(focus_score_fine,fsc)
                    image_result.Release()
                    #plt.imshow(image_data)
                    #plt.show()
                    #image_data.Release()

                    elapsed_time = current_time - last_time
                    sleep_time = max(0, frame_time - elapsed_time)
                    time.sleep(sleep_time)  # Sleep for the remaining time if needed



                    last_time = current_time

                fine_target_z = steps_fine[np.argmax(focus_score_fine)]
                steps_final = steps = np.linspace(fine_target_z-step/2,fine_target_z+step/2,21)
                focus_score_final = np.array([])
                for i in range(len(steps_final)):

                    current_time = time.time()

                    device.move.setControlTargetPosition(2,steps_final[i])
                    time.sleep(0.1)

                    image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

                    if image_result.IsIncomplete():
                        print(f"Image incomplete with status {image_result.GetImageStatus()}")
                        image_result.Release()
                        continue

                    # Convert image to a NumPy array
                    image_data = image_result.GetNDArray()

                    #cv.imshow("Camera Feed", image_data)
                        
                        
                        #cv.axvline(500)
                        # Release the image
                    
                    fsc = NG.calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
                    print(fsc)
                    focus_score_final = np.append(focus_score_final,fsc)
                    image_result.Release()
                    #plt.imshow(image_data)
                    #plt.show()
                    #image_data.Release()

                    elapsed_time = current_time - last_time
                    sleep_time = max(0, frame_time - elapsed_time)
                    time.sleep(sleep_time)  # Sleep for the remaining time if needed



                    last_time = current_time


                #coefficients = np.polyfit(fitst,focus_score,2)
                params2, _ = curve_fit(NG.gauss, fitst, focus_score_fine, p0=initial_guesses)
                print(params2)

                params3, _ = curve_fit(NG.gauss, fitst, focus_score_final, p0=initial_guesses)
                print(params3)



                target_z = steps_final[0] + params3[1] * (steps_final[1]-steps_final[0])
                device.move.setControlTargetPosition(2,target_z)


                print('zoinks')

                if abs(target_z) > z_lim:
                    focus_stab=False 

                fig2.data[0].x = fitst
                fig2.data[0].y = focus_score_final
                plot_element2.update()
                continue  #
            #except:
                #cam.EndAcquisition()
                #cam.DeInit()
            
            
            #fsdata = focus_scan(2000,frame_time,last_time)
            #fig2.update_layout(shapes=[dict(type='line', y0=y_max, y1=y_max, x0=0, x1=1, xref='paper', yref='y')])
        

            # Update the plot with new data
        

            

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
        fig.update_layout(shapes=[dict(type='line', y0=y_max, y1=y_max, x0=0, x1=1, xref='paper', yref='y')])
        

        # Update the plot with new data
        fig.data[0].x = x_data
        fig.data[0].y = y_data
        plot_element.update()  # This correctly triggers the update of the Plotly plot

        if savefigs == True and counter % save_n_frames == 0:
            savetime = np.round(time.time(),2)
            filename = folder + str(counter) + '-' + str(savetime).split('.')[0] + 'p' + str(savetime).split('.')[1] +  '.pgm'
            cv2.imwrite(filename,image_data)
        
        
        image_result.Release()

         
        counter += 1

        # Sleep for a short time before updating again
        elapsed_time = current_time - last_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)  # Sleep for the remaining time if needed

        last_time = current_time
    try:
        image_result.Release()
    except:
        print('No image to release')
    cv2.destroyAllWindows()
    cam.EndAcquisition()
    print("Acquisition stopped.")
    cam.DeInit()

def focus_scan(step,frametime,lasttime):
    global cam, device
    print("entering focus scan!")
    curr_z = device.control.getPositionsAndVoltages()[2]
    #print('a')
    steps = np.linspace(curr_z-10*step,curr_z+10*step,21)
    #print('b')
    
    frame_time = frametime#1.0 / frame_rate  # Time between frames (in seconds)
    last_time = lasttime

    focus_score = np.array([])
    #print('c')
    for i in range(len(steps)):

        current_time = time.time()

        device.move.setControlTargetPosition(2,steps[i])
        #print('d')
        time.sleep(0.1)

        image_result = cam.GetNextImage(2000)#15000)  # Timeout in milliseconds
        #print('e')
        if image_result.IsIncomplete():
            print(f"Image incomplete with status {image_result.GetImageStatus()}")
            image_result.Release()
            continue

        # Convert image to a NumPy array
        image_data = image_result.GetNDArray()

        #cv.imshow("Camera Feed", image_data)
            
            
            #cv.axvline(500)
            # Release the image
        
        fsc = calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
        #print(fsc)
        focus_score = np.append(focus_score,fsc)
        image_result.Release()
        #plt.imshow(image_data)
        #plt.show()
        #image_data.Release()

        elapsed_time = current_time - last_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)  # Sleep for the remaining time if needed



        last_time = current_time

    
    
    print('hooray')
    print(focus_score)
    device.move.setControlTargetPosition(2,curr_z)

    time.sleep(0.2)


    maxind = np.argmax(focus_score)
    fitst = np.linspace(0,20,21)
    # Initial guesses based on visual inspection 
    initial_guesses = [-5000,10,1000000]

    

# Fit the parabola
    params, _ = curve_fit(NG.parabola, fitst, focus_score, p0=initial_guesses)
    print(params)

    rough_target_z = steps[0] + params[1] * (steps[1]-steps[0])
    device.move.setControlTargetPosition(2,rough_target_z)


    steps_fine = steps = np.linspace(rough_target_z-10*step/5,rough_target_z+10*step/5,21)
    focus_score_fine = np.array([])
    #time.sleep(0.2)
    for i in range(len(steps_fine)):

        current_time = time.time()

        device.move.setControlTargetPosition(2,steps_fine[i])
        time.sleep(0.1)

        image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

        if image_result.IsIncomplete():
            print(f"Image incomplete with status {image_result.GetImageStatus()}")
            image_result.Release()
            continue

        # Convert image to a NumPy array
        image_data = image_result.GetNDArray()

        #cv.imshow("Camera Feed", image_data)
            
            
            #cv.axvline(500)
            # Release the image
        
        fsc = calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
        print(fsc)
        focus_score_fine = np.append(focus_score_fine,fsc)
        image_result.Release()
        #plt.imshow(image_data)
        #plt.show()
        #image_data.Release()

        elapsed_time = current_time - last_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)  # Sleep for the remaining time if needed



        last_time = current_time

    fine_target_z = steps_fine[np.argmax(focus_score_fine)]
    steps_final = steps = np.linspace(fine_target_z-step/2,fine_target_z+step/2,21)
    focus_score_final = np.array([])
    for i in range(len(steps_final)):

        current_time = time.time()

        device.move.setControlTargetPosition(2,steps_final[i])
        time.sleep(0.1)

        image_result = cam.GetNextImage()#15000)  # Timeout in milliseconds

        if image_result.IsIncomplete():
            print(f"Image incomplete with status {image_result.GetImageStatus()}")
            image_result.Release()
            continue

        # Convert image to a NumPy array
        image_data = image_result.GetNDArray()

        #cv.imshow("Camera Feed", image_data)
            
            
            #cv.axvline(500)
            # Release the image
        
        fsc = calculate_focus_score(image_data[fy1:fy2,fx1:fx2],5)
        print(fsc)
        focus_score_final = np.append(focus_score_final,fsc)
        image_result.Release()
        #plt.imshow(image_data)
        #plt.show()
        #image_data.Release()

        elapsed_time = current_time - last_time
        sleep_time = max(0, frame_time - elapsed_time)
        time.sleep(sleep_time)  # Sleep for the remaining time if needed



        last_time = current_time


    #coefficients = np.polyfit(fitst,focus_score,2)
    params2, _ = curve_fit(NG.parabola, fitst, focus_score_fine, p0=initial_guesses)
    print(params2)

    params3, _ = curve_fit(NG.parabola, fitst, focus_score_final, p0=initial_guesses)
    print(params3)



    target_z = steps_final[0] + params3[1] * (steps_final[1]-steps_final[0])
    device.move.setControlTargetPosition(2,target_z)

    return fitst, focus_score_final, target_z




# Start the data update in a separate thread
thread2 = threading.Thread(target=update_image2, daemon=True)
thread2.start()

# Create the NiceGUI layout
def create_gui():
    
    # Use ui.column() and ui.row() directly without using .add()

   # with ui.grid(columns=16).classes('w-full gap-0'):
   #     plot_element.classes('col-span-8 border p-1')
   #     plot_element2.classes('col-span-8 border p-1')
    #    ui.label('8').classes('col-span-4 border p-1')
   #     ui.button('bbbbbbbbbb me!', on_click=lambda: ui.notify('You clicked me!')).classes('col-span-4 border p-1')
    #    ui.label('8').classes('col-span-8 border p-1')
    with ui.row():
        with ui.column():

            plot_element
    #    ui.button('bbbbbbbbbb me!', on_click=lambda: ui.notify('You clicked me!'))
        with ui.column():
            plot_element2

        #with ui.column():
         #   plot_element
        #with ui.column():
  
            
     

    # Run the NiceGUI app
    ui.run()

# Run the NiceGUI app
create_gui()
