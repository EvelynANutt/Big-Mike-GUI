""" Top header """
import tkinter as tk
from PIL import ImageTk, Image

class Header:
    frame: tk.Frame

    def experiment_window(self):
        top = tk.Toplevel()
        top.title("Big Mike GUI - Experiment Setup")
        frame = tk.Label(top, borderwidth=5, relief='solid')
        header = tk.Frame(frame)
        title = tk.Label(header, text='Capture', font=('Aria',26))

    def properties_window(self):
        top = tk.Toplevel()
        top.title("Big Mike GUI - System Properties")
        frame = tk.Label(top, borderwidth=5, relief='solid')
        header = tk.Frame(frame)
        title = tk.Label(header, text='Capture', font=('Aria',26))
    
    def processing_window(self):
        top = tk.Toplevel()
        top.title("Big Mike GUI - Post-Processing")
        frame = tk.Label(top, borderwidth=5, relief='solid')
        header = tk.Frame(frame)
        title = tk.Label(header, text='Capture', font=('Aria',26))

    def __init__(self, parent):
        # Create frame
        self.frame = tk.Frame(parent)

        # Logo label
        logo_img = Image.open('/Users/evelynanutt/GitHub/Big-Mike-GUI/src/bigmike_logo.png')
        self.logo_img = ImageTk.PhotoImage(logo_img.resize((100,100)))
        self.logo = tk.Label(self.frame, image=self.logo_img)

        # Tabs label
        self.tabs = tk.Frame(self.frame)
        self.experiment_setup_tab = tk.Button(self.tabs, text='Experiment Setup', font=('Aria',26), command=self.experiment_window)
        self.system_properties_tab = tk.Button(self.tabs, text='System Properties', font=('Aria',26), command=self.properties_window)
        self.post_processing_tab = tk.Button(self.tabs, text='Post-Processing', font=('Aria',26), command=self.processing_window)
        
    def render(self):
        self.logo.pack(side='left')
        self.experiment_setup_tab.pack(side='left', fill='both', expand=True)
        self.system_properties_tab.pack(side='left', fill='both', expand=True)
        self.post_processing_tab.pack(side='left', fill='both', expand=True)
        self.tabs.pack(side='left', fill='both', expand=True)
        self.frame.pack(fill='both')
