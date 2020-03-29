from View.GuiBuilder.Base import *


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

