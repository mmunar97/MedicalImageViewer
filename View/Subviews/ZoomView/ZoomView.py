from tkinter import messagebox

import cv2
import threading
from View.GuiBuilder.Layouts.Subviews.MeasureDistanceZoomLayout import *
from View.Subviews.ZoomView.ZoomedImageViewer import ZoomedImageViewer


class ZoomView(tk.Frame, threading.Thread):

    def __init__(self, root_view: tk.Toplevel,
                 initial_image: numpy.ndarray,
                 *args, **kwargs):
        threading.Thread.__init__(self)
        tk.Frame.__init__(self, *args, **kwargs)

        self.__root_view = root_view

        # IMAGE VIEW
        self.__loaded_image_raw = initial_image
        self.__modified_image = initial_image.copy()

        self.__loaded_image = build_photo_image(self.__loaded_image_raw)
        self.__image_view, self.__loaded_image_view = build_canvas_image_viewer(self.__root_view,
                                                                                self.__loaded_image)

        # TOOLS FRAME
        self.__tool_frame = build_tools_frame(self.__root_view)

        self.__point1_coordinate_selector_title = build_point_selector_title(root_view=self.__root_view,
                                                                             label_title="FIRST POINT COORDINATES",
                                                                             origin=(900, 30))

        # TOOLS
        self.__point1_x_subtitle = build_point_selector_subtitle(root_view=self.__root_view,
                                                                 label_title="X VALUE SELECTOR",
                                                                 origin=(900, 55))
        self.__point1_y_subtitle = build_point_selector_subtitle(root_view=self.__root_view,
                                                                 label_title="Y VALUE SELECTOR",
                                                                 origin=(900, 120))

        self.__point1_x_value, self.__point1_y_value = build_point_variables()
        self.__point1_x_slider = build_point_slider(root_view=self.__root_view,
                                                    sliding_range=(0, self.__loaded_image_raw.shape[1] - 1),
                                                    variable=self.__point1_x_value,
                                                    command=self.slider_value_did_change,
                                                    coordinates=(900, 75))
        self.__point1_y_slider = build_point_slider(root_view=self.__root_view,
                                                    sliding_range=(0, self.__loaded_image_raw.shape[0] - 1),
                                                    variable=self.__point1_y_value,
                                                    command=self.slider_value_did_change,
                                                    coordinates=(900, 140))

        self.__point2_coordinate_selector_title = build_point_selector_title(root_view=self.__root_view,
                                                                             label_title="SECOND POINT COORDINATES",
                                                                             origin=(900, 190))

        self.__point2_x_subtitle = build_point_selector_subtitle(root_view=self.__root_view,
                                                                 label_title="X VALUE SELECTOR",
                                                                 origin=(900, 215))
        self.__point2_y_subtitle = build_point_selector_subtitle(root_view=self.__root_view,
                                                                 label_title="Y VALUE SELECTOR",
                                                                 origin=(900, 280))

        self.__point2_x_value, self.__point2_y_value = build_point_variables()
        self.__point2_x_slider = build_point_slider(root_view=self.__root_view,
                                                    sliding_range=(0, self.__loaded_image_raw.shape[1] - 1),
                                                    variable=self.__point2_x_value,
                                                    command=self.slider_value_did_change,
                                                    coordinates=(900, 235))
        self.__point2_y_slider = build_point_slider(root_view=self.__root_view,
                                                    sliding_range=(0, self.__loaded_image_raw.shape[0] - 1),
                                                    variable=self.__point2_y_value,
                                                    command=self.slider_value_did_change,
                                                    coordinates=(900, 300))

        self.__apply_zoom_button = build_zoom_button(root_view=self.__root_view,
                                                     button_title="  Show region  ",
                                                     command=self.show_zoom_image,
                                                     coordinates=(980, 370))

    def slider_value_did_change(self, _):
        """
        Detects when the sliders have changed, and updates the view with the information.
        """
        self.__modified_image = self.__loaded_image_raw.copy()

        point1_x = self.__point1_x_value.get()
        point1_y = self.__point1_y_value.get()

        point2_x = self.__point2_x_value.get()
        point2_y = self.__point2_y_value.get()

        self.__modified_image = cv2.rectangle(self.__modified_image,
                                              (point1_x, point1_y),
                                              (point2_x, point2_y),
                                              (255, 0, 0),
                                              1)

        self.__modified_image = cv2.circle(self.__modified_image,
                                           (point1_x, point1_y),
                                           3,
                                           (255, 0, 0),
                                           4)

        self.__modified_image = cv2.circle(self.__modified_image,
                                           (point2_x, point2_y),
                                           3,
                                           (200, 200, 200),
                                           4)

        self.__loaded_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.__modified_image))
        self.__image_view.itemconfig(self.__loaded_image_view, image=self.__loaded_image)
        self.__root_view.update()

    def show_zoom_image(self):
        point1_x = self.__point1_x_value.get()
        point1_y = self.__point1_y_value.get()

        point2_x = self.__point2_x_value.get()
        point2_y = self.__point2_y_value.get()

        if point1_x == point2_x or point1_y == point2_y:
            messagebox.showerror("Error", "Selected region must be two dimensional")
        else:
            zoom_image = self.__loaded_image_raw[point2_y: point1_y, point2_x:point1_x]

            zoom_image_root_view = tk.Toplevel(self)
            zoom_image_root_view.resizable(False, False)
            zoom_image_root_view.title("Zoomed image")
            zoom_image_view = ZoomedImageViewer(zoom_image_root_view,
                                                zoom_image)
            zoom_image_root_view.geometry("870x610+90+90")

