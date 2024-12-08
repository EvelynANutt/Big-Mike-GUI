import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

class Histogram:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, background="pink")

        # Initialize the camera
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Error: Unable to access the camera.")
            exit()

        plt.rcParams.update({
            'font.size': 4,               # Overall font size
            'axes.titlesize': 5,        # Title font size
            'axes.labelsize': 4,         # Axis label font size
            'xtick.labelsize': 3,        # X-axis tick font size
            'ytick.labelsize': 3,        # Y-axis tick font size
            'legend.fontsize': 4,        # Legend font size
            'figure.figsize': (4, 2),    # Figure size
        })

        # Set up Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_title("Live RGB Histogram")
        self.ax.set_xlabel("Pixel Intensity")
        self.ax.set_ylabel("Log(Number of Pixels)")
        self.ax.set_xlim(0, 255)
        self.ax.set_yscale("log")  # Set Y-axis to logarithmic scale
        self.ax.grid(alpha=0.5)
        self.blue_line, = self.ax.plot([], [], color="blue", label="Blue Channel")
        self.green_line, = self.ax.plot([], [], color="green", label="Green Channel")
        self.red_line, = self.ax.plot([], [], color="red", label="Red Channel")
        self.ax.legend()

        # Embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        # Start the live histogram update in a separate thread
        self.running = True
        self.thread = threading.Thread(target=self.update_histogram, daemon=True)
        self.thread.start()

    def render(self):
        self.frame.pack(fill='both', expand=True)
        self.canvas_widget.pack(fill='both', expand=True)

    def update_histogram(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame from the camera.")
                self.running = False
                self.cap.release()
                return

            # Split the frame into R, G, and B channels
            blue_channel, green_channel, red_channel = cv2.split(frame)

            # Compute histograms
            bins = 256
            hist_range = [0, 256]
            blue_hist = cv2.calcHist([blue_channel], [0], None, [bins], hist_range).flatten()
            green_hist = cv2.calcHist([green_channel], [0], None, [bins], hist_range).flatten()
            red_hist = cv2.calcHist([red_channel], [0], None, [bins], hist_range).flatten()

            # Update plot data
            self.blue_line.set_data(range(bins), blue_hist)
            self.green_line.set_data(range(bins), green_hist)
            self.red_line.set_data(range(bins), red_hist)

            # Adjust Y-axis limits dynamically for log scale
            self.ax.set_ylim(1, max(blue_hist.max(), green_hist.max(), red_hist.max()))

            # Redraw the plot
            self.canvas.draw()

    def close(self):
        self.running = False
        self.thread.join()
        self.cap.release()
