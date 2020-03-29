from View.GuiBuilder.Base import *
from View.GuiBuilder.Values.Colors import Colors
from View.GuiBuilder.Values.Fonts import Fonts


def build_canvas_image_viewer(root_view: tk.Tk,
                              image: PhotoImage) -> Tuple[tk.Canvas, int]:
    """
    Builds the Canvas that acts as a image viewer.

    Args:
        root_view: The root view of the layout.
        image: A PhotoImage, representing the image to be displayed.

    Returns:
        A tuple of two elements, containing the initialized canvas and the integer value of the associated
        image with the canvas.
    """
    return build_canvas_with_image(root_view=root_view,
                                   image=image,
                                   size=(870, 610),
                                   coordinates=(0, 0))


def build_tools_frame(root_view: tk.Tk) -> tk.Frame:
    """
    Builds the frame that will contain the different tools for measure distance.

    Args:
        root_view: The root view of the layout.

    Returns:
        The initialized frame.
    """
    return build_frame(root_view=root_view,
                       background_color=Colors.TOOLS_PANEL_BACKGROUND,
                       size=(300, 700),
                       coordinates=(880, 0))


def build_point_selector_title(root_view: tk.Tk,
                               label_title: str,
                               origin: Tuple[int, int]) -> tk.Label:
    """
    Builds a title label.

    Args:
        root_view: The root view of the layout.
        label_title: A string, representing the text to show.
        origin: A tuple of two values, representing the coordinates of the origin.

    Returns:
        A tk.Label object.
    """
    return build_label(root_view=root_view,
                       text=label_title,
                       font=Fonts.BOLD.value,
                       background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                       coordinates=origin)


def build_point_selector_subtitle(root_view: tk.Tk,
                                  label_title: str,
                                  origin: Tuple[int, int]) -> tk.Label:
    """
    Builds a title label.

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


def build_point_variables() -> Tuple[tk.IntVar, tk.IntVar]:
    """
    Generates the variables that will store the variables of two sliders.

    Returns:
        A tuple of two IntVar objects.
    """
    return tk.IntVar(), tk.IntVar()


def build_point_slider(root_view: tk.Tk,
                       sliding_range: Tuple[int, int],
                       variable: tk.IntVar,
                       command: Callable,
                       coordinates: Tuple[int, int]) -> tk.Scale:
    """
    Builds a slider.

    Args:
        root_view: The root view of the layout.
        sliding_range: A tuple of two elements, containing the range of sliding.
        variable: An IntVar object, representing the object that stores the value when the slider changes.
        command: A Callable method, representing the event when the slider changes.
        coordinates: A tuple of two elements, containing the position of the entry in format (x,y).

    Returns:
        A slider.
    """
    return build_slider(root_view=root_view,
                        sliding_range=sliding_range,
                        background_color=Colors.TOOLS_PANEL_BACKGROUND,
                        variable=variable,
                        command=command,
                        length=250,
                        enabled=True,
                        coordinates=coordinates)


def build_zoom_button(root_view: tk.Tk,
                      button_title: str,
                      command: Callable,
                      coordinates: Tuple[int, int]) -> tk.Button:
    """

    Args:
        root_view:
        button_title:
        command:
        coordinates:

    Returns:

    """
    return build_button(root_view=root_view,
                        button_text=button_title,
                        command=command,
                        coordinates=coordinates,
                        enabled=True)
