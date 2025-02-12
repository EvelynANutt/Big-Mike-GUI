import tkinter as tk
from PIL import ImageTk, Image
from header import Header
from obs_deck.body import Body
from business.store import Store

def main():
    # Create the main window & size
    window = tk.Tk()
    window.title('Big Mike GUI')
    window.geometry('1200x800')

    # Create the store
    store = Store()
    
    # # Create the header
    header = Header(window)
    header.render()

    # # Create the body
    body = Body(window, store)
    body.render()
    
    # # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()