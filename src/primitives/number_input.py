""" Any number input setting """
import tkinter as tk
from typing import Callable

class NumberInput:
    frame: tk.Frame
    title: str
    
    def edit_num_entry():
        print (1 + 1)

    def __init__(self, parent, title, command_plus: Callable, command_minus: Callable):
        # Create frame
        self.frame = tk.Label(parent)
        self.title = title
        self.minus_button = tk.Button(self.frame, text='-', font=('Aria',16), command=command_minus)
        self.value = tk.StringVar()
        self.value.set("0.0")
        self.number_entry = tk.Entry(self.frame, justify='center', textvariable=self.value, font=('Aria',20))
        self.plus_button = tk.Button(self.frame, text='+', font=('Aria',16), command=command_plus)
        self.title_label = tk.Label(self.frame, text=self.title, font=('Aria',20))

    def render(self):
        self.minus_button.pack(side='left')
        self.number_entry.pack(side='left')
        self.plus_button.pack(side='left')
        self.title_label.pack(side='left')
        self.frame.pack(fill='x', expand=True)
    