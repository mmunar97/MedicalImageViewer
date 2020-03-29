import PIL
import numpy
from PIL.ImageTk import PhotoImage
import tkinter as tk
from View.GuiBuilder.Values.Colors import Colors
from typing import Callable, Tuple

from PIL.ImageTk import PhotoImage


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


def build_frame(root_view: tk.Tk,
                background_color: Colors,
                size: Tuple[int, int],
                coordinates: Tuple[int, int]) -> tk.Frame:
    """
    Builds a frame.

    Args:
        root_view: The root view of the layout.
        background_color: A Colors object, containing the background color.
        size: A tuple, containing the size of the entry in format (w,h).
        coordinates: A tuple, containing the position of the entry in format (x,y).

    Returns:
        A Frame object.
    """
    frame = tk.Frame(root_view,
                     bg=background_color.value,
                     width=size[0],
                     height=size[1])
    frame.place(x=coordinates[0], y=coordinates[1])
    return frame


def build_canvas_with_image(root_view: tk.Tk,
                            image: PhotoImage,
                            size: Tuple[int, int],
                            coordinates: Tuple[int, int]) -> Tuple[tk.Canvas, int]:
    """
    Builds a canvas with an image.

    Args:
        root_view: The root view of the layout.
        image: A PhotoImage, containing the image to be shown.
        size: A tuple, containing the size of the entry in format (w,h).
        coordinates: A tuple, containing the position of the entry in format (x,y).

    Returns:

    """
    image_view = tk.Canvas(root_view,
                           width=size[0],
                           height=size[1])
    loaded_image_view = image_view.create_image(0, 0, image=image, anchor=tk.NW)
    image_view.image = image
    image_view.pack()
    image_view.place(x=coordinates[0], y=coordinates[1])
    return image_view, loaded_image_view


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


def build_slider(root_view: tk.Tk,
                 sliding_range: Tuple[float, float],
                 background_color: Colors,
                 variable: tk.IntVar,
                 command: Callable,
                 length: int,
                 enabled: bool,
                 coordinates: Tuple[int, int]) -> tk.Scale:
    """
    Builds an slider from its main components.

    Args:
        root_view: The root view of the layout.
        sliding_range: A tuple of two elements, containing the limits of the slider.
        background_color: A Colors object, containing the background color.
        variable: A IntVar, representing the object that stores the value of the slider.
        command: A Callable, representing the function that detects when the slider has changed its value.
        length: An integer, representing the length of the slider.
        enabled: A boolean, indicating if the slider is enabled to user interaction.
        coordinates: A tuple of two elements, containing the position of the entry in format (x,y).

    Returns:

    """
    slider = tk.Scale(root_view,
                      from_=sliding_range[0],
                      to=sliding_range[1],
                      orient=tk.HORIZONTAL,
                      bg=background_color.value,
                      variable=variable,
                      command=command,
                      length=length)
    slider.pack()
    slider.place(x=coordinates[0], y=coordinates[1])

    if enabled:
        slider.configure(state='active')
    else:
        slider.configure(state='disabled')

    return slider


def build_photo_image(image: numpy.ndarray) -> PhotoImage:
    """
    Builds the photo image from its matrix representation.

    Args:
        image: A numpy ndarray, representing the image as matrix.

    Returns:
        A PhotoImage, containing the image to be shown in a Canvas.
    """
    return PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))


def build_button(root_view: tk.Tk,
                 button_text: str,
                 command: Callable,
                 coordinates: Tuple[int, int],
                 enabled: bool) -> tk.Button:
    """
    Builds a button from its main components.

    Args:
        root_view: The root view of the layout.
        button_text: The text that the button will display.
        command: A Callable, representing the function that manages the event.
        coordinates: A tuple of two elements, containing the position of the entry in format (x,y).
        enabled: A boolean, indicating if the slider is enabled to user interaction.

    Returns:
        A tk.Button object.
    """
    button = tk.Button(root_view,
                       text=button_text,
                       compound="left",
                       highlightbackground=Colors.TOOLS_PANEL_BACKGROUND.value,
                       command=command)
    button.pack()
    button.place(x=coordinates[0], y=coordinates[1])
    if enabled:
        button.configure(state='active')
    else:
        button.configure(state='disabled')

    return button
