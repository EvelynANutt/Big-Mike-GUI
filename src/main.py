import tkinter as tk
from PIL import ImageTk, Image
import os

def on_click():
    print("YEEEEEEEEEEEEEEEEAAAAAH")

def main():
    # Create the main window
    root = tk.Tk()
    
    # Create a label widget
    label = tk.Label(root, text='Observation Deck')
    label.place(relx=0.5,
                rely=0.5,
                anchor='n')

    # Load the logo image
    logo = Image.open('/Users/evelynanutt/GitHub/Big-Mike-GUI/src/bigmike_logo.png')
    resize_logo = logo.resize((200,200))
    logo_img = ImageTk.PhotoImage(resize_logo)
    # Read the logo image
    logo_panel = tk.Label(root, image=logo_img)
    logo_panel.place(anchor='nw')

    # Create a button
    button = tk.Button(root, text="Click me!", command=on_click)
    button.place(anchor='ne')
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()