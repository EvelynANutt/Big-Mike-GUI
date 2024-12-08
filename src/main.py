import tkinter as tk
from PIL import ImageTk, Image

from header import Header
from obs_deck.body import Body

def main():
    # Create the main window & size
    window = tk.Tk()
    window.title('Big Mike GUI')
    window.geometry('1200x800')
    
    # Create the header
    header = Header(window)
    header.render()

    # Create the body
    body = Body(window)
    body.render()
    
    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()