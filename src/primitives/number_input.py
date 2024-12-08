""" Any number input setting """
import tkinter as tk

class NumberInput:
    frame: tk.Frame
    title: str

    def __init__(self, parent, title):
        # Create frame
        self.frame = tk.Label(parent)
        self.title = title
        self.minus_button = tk.Button(self.frame, text='-', font=('Aria',16))
        self.value = tk.StringVar()
        self.value.set("0.0")
        self.number_entry = tk.Entry(self.frame, justify='center', textvariable=self.value, font=('Aria',20))
        self.plus_button = tk.Button(self.frame, text='+', font=('Aria',16))
        self.title_label = tk.Label(self.frame, text=self.title, font=('Aria',20))

    def render(self):
        self.minus_button.pack(side='left')
        self.number_entry.pack(side='left')
        self.plus_button.pack(side='left')
        self.title_label.pack(side='left')
        self.frame.pack(fill='x', expand=True)