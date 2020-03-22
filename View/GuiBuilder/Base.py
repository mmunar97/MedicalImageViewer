import tkinter as tk
from typing import Tuple


def build_label(root_view: tk.Tk,
                text: str,
                font: str,
                background_color: str,
                coordinates: Tuple[int, int]) -> tk.Label:
    """
    Builds a label from its main components.

    Args:
        root_view: The root view of the layout.
        text: A string, representing the text that will contain the label.
        font: A string, representing the font to be used.
        background_color: A string, representing the background color of the label in hexadecimal representation.
        coordinates: A tuple, containing the position of the label in format (x,y).

    Returns:
        A tk.Label object.
    """
    label = tk.Label(root_view,
                     text=text,
                     font=font,
                     bg=background_color)

    label.pack()
    label.place(x=coordinates[0], y=coordinates[1])
    return label


def build_edit_text(root_view: tk.Tk,
                    placeholder: str,
                    coordinates: Tuple[int, int],
                    size: Tuple[int, int]) -> tk.Entry:
    """
    Builds an entry from its main components.

    Args:
        root_view: The root view of the layout.
        placeholder: A string, representing the initial text that will be displayed in the entry.
        coordinates: A tuple, containing the position of the entry in format (x,y).
        size: A tuple, containing the size of the entry in format (w,h).

    Returns:
        A tk.Entry object,
    """
    entry = tk.Entry(root_view)
    entry.pack()
    entry.place(x=coordinates[0], y=coordinates[1], width=size[0], height=size[1])
    entry.insert(0, placeholder)
    return entry
