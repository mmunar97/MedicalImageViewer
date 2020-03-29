import cv2
import threading
from PIL import Image, ImageTk
from View.GuiBuilder.Layouts.Subviews.MeasureDistanceZoomLayout import *


class ProjectionsView(tk.Frame, threading.Thread):

    def __init__(self, root_view: tk.Toplevel,
                 initial_image: numpy.ndarray,
                 *args, **kwargs):
        pass
