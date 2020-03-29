from tkinter import messagebox

import cv2
import threading
from View.GuiBuilder.Layouts.Subviews.MeasureDistanceZoomLayout import *


class ZoomedImageViewer(tk.Frame, threading.Thread):

    def __init__(self, root_view: tk.Toplevel,
                 initial_image: numpy.ndarray,
                 *args, **kwargs):
        threading.Thread.__init__(self)
        tk.Frame.__init__(self, *args, **kwargs)

        self.__root_view = root_view
        self.__loaded_image_raw = cv2.resize(initial_image,
                                             (870, 610),
                                             interpolation=cv2.INTER_AREA)

        self.__loaded_image = build_photo_image(self.__loaded_image_raw)
        self.__image_view, self.__loaded_image_view = build_canvas_image_viewer(self.__root_view,
                                                                                self.__loaded_image)
