""" Stage control """
import tkinter as tk
from primitives.number_input import NumberInput
from business.store import Store

dim_to_letter = {
    0: 'x',
    1: 'y',
    2: 'z'
}

class StageControlInput:
    frame: tk.Frame

    def __init__(self, parent, store: Store, dim: int):
        # Store the store
        self.store = store
        self.dim = dim
        self.scale = 1000

        # Create frame
        self.frame = tk.Label(parent, borderwidth=5, relief='solid')

        # Header frame
        self.header = tk.Frame(self.frame)
        self.title = tk.Label(self.header, text='Stage Controls', font=('Aria',26))

        # xyz translation and xy cropping names
        self.input = NumberInput(self.frame, 
                                 default_entry=self.store.attocube.get_value(dim), 
                                 title=f'{dim_to_letter[dim]} [nm]', 
                                 command_set_up=self.update, 
                                 command_set_down=self.update, 
                                 command_set_abs=self.update,
                                 increment=self.scale)

    def update(self):
        value = float(self.input.value.get())
        self.store.attocube.set_value(self.dim, value)
        new_value = self.store.attocube.get_value(self.dim)
        self.input.value.set(str(new_value))

    def render(self):
        self.input.render()