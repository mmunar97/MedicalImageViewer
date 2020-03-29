import tkinter as tk

from View.GuiBuilder.Base import *
from View.GuiBuilder.Values.Colors import Colors
from View.GuiBuilder.Values.Fonts import Fonts


def build_contrast_adjustment_title(root_view: tk.Tk) -> tk.Label:
    """
    Builds the title of the section.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tk.Label object.
    """
    return build_label(root_view=root_view,
                       text="CONTRAST ADJUSTMENT",
                       font=Fonts.BOLD.value,
                       background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                       coordinates=(920, 490))


def build_contrast_selector_subtitle(root_view: tk.Tk,
                                     label_title: str,
                                     origin: Tuple[int, int]) -> tk.Label:
    """
    Builds a subtitle label.

    Args:
        root_view: The root view of the layout.
        label_title: A string, representing the text to show.
        origin: A tuple of two values, representing the coordinates of the origin.

    Returns:
        A tk.Label object.
    """
    return build_label(root_view=root_view,
                       text=label_title,
                       font=Fonts.REGULAR.value,
                       background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                       coordinates=origin)


def build_contrast_selector_slider(root_view: tk.Tk,
                                   sliding_range: Tuple[int, int],
                                   command: Callable,
                                   coordinates: Tuple[int, int]) -> Tuple[tk.IntVar, tk.Scale]:
    """
    Builds the slider and initializes the variable that will contain its value.

    Args:
        root_view: The root view of the layout.
        sliding_range: A tuple of two elements, containing the range of sliding.
        command: A Callable method, representing the event when the slider changes.
        coordinates: A tuple of two elements, containing the position of the entry in format (x,y).

    Returns:
        A tuple of two elements, containing the variable that contains the value of the slider and the slider.
    """
    variable = tk.IntVar()
    slider = build_slider(root_view=root_view,
                          sliding_range=sliding_range,
                          background_color=Colors.TOOLS_PANEL_BACKGROUND,
                          variable=variable,
                          command=command,
                          length=250,
                          enabled=False,
                          coordinates=coordinates)

    return variable, slider
