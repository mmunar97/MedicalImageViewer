import cv2
import threading
from PIL import Image, ImageTk

from Controller.ListenerCode import ListenerCode
from View import GUI
from View.GuiBuilder.Layouts.Subviews.MeasureDistanceZoomLayout import *


class MeasureDistanceView(tk.Frame, threading.Thread):

    def __init__(self,
                 root_view: tk.Toplevel,
                 parent_view: GUI,
                 initial_image: numpy.ndarray,
                 pixel_size: Tuple[float, float],
                 *args, **kwargs):
        """
        Initializes the view that shows the tools for measuring distances in the image.

        Args:
            root_view: The root view of this view.
            parent_view: An instance of the GUI parent view.
            initial_image: The image to show, represented as a numpy ndarray.
            pixel_size: A tuple of two elements, representing the correspondence of 1 pixel in millimeters. Contains
                        the equivalence by rows and by columns.
        """
        threading.Thread.__init__(self)
        tk.Frame.__init__(self, *args, **kwargs)

        self.__root_view = root_view
        self.__parent_view = parent_view

        # IMAGE VIEW
        self.__loaded_image_raw = initial_image
        self.__pixel_size = pixel_size
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

        self.__distance_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                    label_title="Euclidean distance",
                                                                    origin=(900, 360))
        self.__distance_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                    label_title="---------",
                                                                    origin=(1050, 360))

        self.__point_1_intensity_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                             label_title="Point 1 intensity",
                                                                             origin=(900, 390))
        self.__point_1_intensity_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                             label_title="---------",
                                                                             origin=(1050, 390))

        self.__point_2_intensity_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                             label_title="Point 2 intensity",
                                                                             origin=(900, 420))
        self.__point_2_intensity_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                             label_title="---------",
                                                                             origin=(1050, 420))

        self.__intensity_difference_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                                label_title="Absolute difference",
                                                                                origin=(900, 450))
        self.__intensity_difference_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                                label_title="---------",
                                                                                origin=(1050, 450))

        self.__region_max_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                      label_title="Region max",
                                                                      origin=(900, 480))
        self.__region_max_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                      label_title="---------",
                                                                      origin=(1050, 480))

        self.__region_argmax_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                         label_title="Region argmax",
                                                                         origin=(900, 510))
        self.__region_argmax_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                         label_title="---------",
                                                                         origin=(1050, 510))

        self.__region_min_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                      label_title="Region min",
                                                                      origin=(900, 540))
        self.__region_min_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                      label_title="---------",
                                                                      origin=(1050, 540))

        self.__region_argmin_title_label = build_point_selector_subtitle(root_view=root_view,
                                                                         label_title="Region argmin",
                                                                         origin=(900, 570))
        self.__region_argmin_value_label = build_point_selector_subtitle(root_view=root_view,
                                                                         label_title="---------",
                                                                         origin=(1050, 570))

    def slider_value_did_change(self, _):
        """
        Detects when the sliders have changed, and updates the view with the information.
        """
        self.__modified_image = self.__loaded_image_raw.copy()

        point1_x = self.__point1_x_value.get()
        point1_y = self.__point1_y_value.get()

        point2_x = self.__point2_x_value.get()
        point2_y = self.__point2_y_value.get()

        self.update_labels((point1_x, point1_y), (point2_x, point2_y))
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

        self.__parent_view.listener(ListenerCode.POINT_DISTANCE_DID_CHANGE,
                                    point1=(point1_x, point1_y),
                                    point2=(point2_x, point2_y))

    def update_labels(self, point_1: Tuple[int, int], point_2: Tuple[int, int]):
        """
        Updates the labels that show the information about the image.

        Args:
            point_1: A point, containing the coordinates of the first point to show.
            point_2: A point, containing the coordinates of the second point to show.

        """

        self.__distance_value_label.config(text=self.compute_distance(point_1, point_2))
        self.__point_1_intensity_value_label.config(text=str(round(self.__loaded_image_raw[point_1[1], point_1[0]], 2)))
        self.__point_2_intensity_value_label.config(text=str(round(self.__loaded_image_raw[point_2[1], point_2[0]], 2)))

        absolute_difference = abs(
            self.__loaded_image_raw[point_1[1], point_1[0]] - self.__loaded_image_raw[point_2[1], point_2[0]])
        self.__intensity_difference_value_label.config(text=str(round(absolute_difference, 2)))

        region = self.__loaded_image_raw[point_2[1]:point_1[1], point_2[0]:point_1[0]]

        try:
            region_max = round(numpy.amax(region), 2)
            region_argmax = numpy.unravel_index(region.argmax(), region.shape)

            self.__region_max_value_label.config(text=str(region_max))
            self.__region_argmax_value_label.config(
                text="(" + str(region_argmax[0] + point_2[0]) + "," + str(region_argmax[1] + point_2[1]) + ")")
        except:
            self.__region_max_value_label.config(text='UNDEF')
            self.__region_argmax_value_label.config(text='UNDEF')

        try:
            region_min = round(numpy.amin(region), 2)
            region_argmin = numpy.unravel_index(region.argmin(), region.shape)

            self.__region_min_value_label.config(text=str(region_min))
            self.__region_argmin_value_label.config(
                text="(" + str(region_argmin[0] + point_2[0]) + "," + str(region_argmin[1] + point_2[1]) + ")")
        except:
            self.__region_min_value_label.config(text='UNDEF')
            self.__region_argmin_value_label.config(text='UNDEF')

    def compute_distance(self, point_1: Tuple[int, int], point_2: Tuple[int, int]) -> str:
        """
        Computes the distance between the two points in millimeters using the equivalence pixel-mm.

        Args:
            point_1: A point, containing the coordinates of the first point to show.
            point_2: A point, containing the coordinates of the second point to show.

        Returns:
            A formatted string, containing the distance and the units.
        """
        increment_x = point_1[0] - point_2[0]
        increment_y = point_1[1] - point_2[1]

        increment_x = increment_x*self.__pixel_size[0]
        increment_y = increment_y*self.__pixel_size[1]

        distance = numpy.linalg.norm((increment_x, increment_y))
        distance = round(distance, 2)

        return str(distance)+" mm"
