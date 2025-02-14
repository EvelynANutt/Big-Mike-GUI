""" Any number input setting """
import tkinter as tk
from typing import Callable

class NumberInput:
    frame: tk.Frame
    title: str

    def __init__(self, parent, title, command_set_up: Callable, command_set_down: Callable, command_set_abs: Callable):
        # Create frame
        self.frame = tk.Label(parent)
        self.title = title
        self.command_set_up = command_set_up
        self.command_set_down = command_set_down
        self.command_set_abs = command_set_abs

        self.minus_button = tk.Button(self.frame, text='-', font=('Aria',16), command=self.move_down)
        self.value = tk.StringVar()
        self.value.set("0.0")
        self.number_entry = tk.Entry(self.frame, justify='center', textvariable=self.value, font=('Aria',20))
        self.number_entry.bind("<FocusIn>", self.on_focus_in)
        self.number_entry.bind("<FocusOut>", self.on_focus_out)
        self.number_entry.bind("<Key>", self.handle_enter)
        self.plus_button = tk.Button(self.frame, text='+', font=('Aria',16), command=self.move_up)
        self.title_label = tk.Label(self.frame, text=self.title, font=('Aria',20))

    def move_up(self):
        new_value = float(self.value.get()) + 1
        self.value.set(str(new_value))
        self.command_set_up()
    
    def move_down(self):
        new_value = float(self.value.get()) - 1
        self.value.set(str(new_value))
        self.command_set_down()
        
    def on_focus_in(self):
        self.old_value = self.value.get()

    def on_focus_out(self):
        self.value.set(self.old_value)

    def handle_enter(self, event: tk.Event):
        if event.keysym == "Return":
            try:
                value_float = float(self.value.get())
            except ValueError:
                value_float = None
            if value_float is None:
                self.value.set(self.old_value)
            else:
                self.old_value = self.value.get()
                self.command_set_abs()

    def render(self):
        self.minus_button.pack(side='left')
        self.number_entry.pack(side='left')
        self.plus_button.pack(side='left')
        self.title_label.pack(side='left', expand=True)
        self.frame.pack(fill='x', expand=True)
    