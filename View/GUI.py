import cv2
import numpy
import threading
import tkinter as tk
import PIL

from Controller.ListenerCode import ListenerCode
from tkinter import *
from tkinter import filedialog
from typing import Any, Callable, List, Tuple
from PIL import Image, ImageTk

from Model.ImageQualityIndicators import ImageQualityIndicators
from View.GuiBuilder.Layouts.MainView import ImageQualityLayout, ContrastAdjustmentLayout
from View.Subviews.ImageMetadataView import ImageMetadataView
from View.Subviews.MeasureDistanceView import MeasureDistanceView
from View.Subviews.ProjectionsView import ProjectionsView
from View.Subviews.ZoomView.ZoomView import ZoomView


class MainView(tk.Frame, threading.Thread):
    tool_panel_background_color = "#999999"

    def __init__(self, root_view: tk.Tk, listener: Callable[[ListenerCode, Any], None], *args, **kwargs):
        """
        Initializes the object that stores the view.

        Args:
            root_view:
            *args:
            **kwargs:
        """
        threading.Thread.__init__(self)
        tk.Frame.__init__(self, *args, **kwargs)

        self.__root_view = root_view
        self.listener = listener

        # BUTTON 1: LOAD IMAGE
        self.__load_image_button_image = ImageTk.PhotoImage(
            Image.open("View/Assets/open_file.png").resize((40, 40), Image.BICUBIC))
        self.__load_image_button = Button(self.__root_view,
                                          text="   Read DICOM   ",
                                          image=self.__load_image_button_image,
                                          compound="left",
                                          command=self.open_file_dialog)
        self.__load_image_button.pack()
        self.__load_image_button.place(x=10, y=10)

        # BUTTON 2: SHOW IMAGE METADATA
        self.__show_image_metadata_button_image = ImageTk.PhotoImage(
            Image.open("View/Assets/explore_metadata.png").resize((40, 40),
                                                                  Image.BICUBIC))

        self.__show_image_metadata_button = Button(self.__root_view,
                                                   text="   Show metadata   ",
                                                   image=self.__show_image_metadata_button_image,
                                                   compound="left",
                                                   command=self.load_image_metadata)
        self.__show_image_metadata_button.pack()
        self.__show_image_metadata_button.place(x=160, y=10)
        self.__show_image_metadata_button.configure(state='disabled')

        # BUTTON 3: MEASURE DISTANCES
        self.__measure_distance_button_image = ImageTk.PhotoImage(
            Image.open("View/Assets/measure_distance.png").resize((40, 40),
                                                                  Image.BICUBIC))
        self.__measure_distance_button = Button(self.__root_view,
                                                text="    Measure distance   ",
                                                image=self.__measure_distance_button_image,
                                                compound="left",
                                                command=self.show_measure_distance_view)
        self.__measure_distance_button.pack()
        self.__measure_distance_button.place(x=325, y=10)
        self.__measure_distance_button.configure(state='disabled')

        self.__measure_distance_root_view = None
        self.__measure_distance_view = None

        # BUTTON 4: ZOOM
        self.__zoom_button_image = ImageTk.PhotoImage(
            Image.open("View/Assets/zoom.png").resize((40, 40),
                                                      Image.BICUBIC))
        self.__zoom_button = Button(self.__root_view,
                                    text="    Zoom  ",
                                    image=self.__zoom_button_image,
                                    compound="left",
                                    command=self.show_zoom_view)
        self.__zoom_button.pack()
        self.__zoom_button.place(x=505, y=10)
        self.__zoom_button.configure(state='disabled')

        self.__zoom_root_view = None
        self.__zoom_view = None

        # BUTTON 5: PROJECTIONS
        # self.__projections_button_image = ImageTk.PhotoImage(
        #     Image.open("View/Assets/projections.png").resize((40, 40),
        #                                                      Image.BICUBIC))
        # self.__projections_button = Button(self.__root_view,
        #                                    text="    Projections  ",
        #                                    image=self.__projections_button_image,
        #                                    compound="left",
        #                                    command=self.show_projections_view)
        # self.__projections_button.pack()
        # self.__projections_button.place(x=610, y=10)
        # self.__projections_button.configure(state='disabled')
        #
        # self.__projections_root_view = None
        # self.__projections_view = None

        # BUTTON 5: EXIT PROGRAM
        self.__exit_button_image = ImageTk.PhotoImage(Image.open("View/Assets/logout.png").resize((40, 40),
                                                                                                  Image.BICUBIC))
        self.__exit_button = Button(self.__root_view,
                                    text="   Exit   ",
                                    image=self.__exit_button_image,
                                    compound="left",
                                    command=self.quit)
        self.__exit_button.pack()
        self.__exit_button.place(x=610, y=10)

        # CREATE TOOL FRAME
        self.__tool_frame = Frame(self.__root_view, bg=self.tool_panel_background_color, width=300, height=700)
        self.__tool_frame.place(x=900, y=0)

        # SLICES COMPONENTS
        self.__slices_label = Label(self.__root_view,
                                    text="SLICE VIEWER",
                                    font='System 14 bold',
                                    bg=self.tool_panel_background_color)
        self.__slices_label.pack()
        self.__slices_label.place(x=920, y=10)

        self.__radio_button_value = IntVar()
        self.__radio_button_x_axis = Radiobutton(self.__root_view,
                                                 text="X axis",
                                                 bg=self.tool_panel_background_color,
                                                 variable=self.__radio_button_value,
                                                 value=0,
                                                 command=self.radio_button_did_switch)
        self.__radio_button_x_axis.pack()
        self.__radio_button_x_axis.place(x=920, y=40)
        self.__radio_button_x_axis.configure(state='disabled')

        self.__radio_button_y_axis = Radiobutton(self.__root_view,
                                                 text="Y axis",
                                                 bg=self.tool_panel_background_color,
                                                 variable=self.__radio_button_value,
                                                 value=1,
                                                 command=self.radio_button_did_switch)
        self.__radio_button_y_axis.pack()
        self.__radio_button_y_axis.place(x=1000, y=40)
        self.__radio_button_y_axis.configure(state='disabled')

        self.__radio_button_z_axis = Radiobutton(self.__root_view,
                                                 text="Z axis",
                                                 bg=self.tool_panel_background_color,
                                                 variable=self.__radio_button_value,
                                                 value=2,
                                                 command=self.radio_button_did_switch)
        self.__radio_button_z_axis.pack()
        self.__radio_button_z_axis.place(x=1080, y=40)
        self.__radio_button_z_axis.configure(state='disabled')

        self.__slice_slider_value = IntVar()
        self.slice_slider = Scale(self.__root_view,
                                  from_=0, to=42,
                                  orient=HORIZONTAL,
                                  bg=self.tool_panel_background_color,
                                  variable=self.__slice_slider_value,
                                  command=self.slider_value_did_change,
                                  length=250)
        self.slice_slider.pack()
        self.slice_slider.place(x=920, y=65)
        self.slice_slider.configure(state='disabled')

        self.__cinema_mode = Label(self.__root_view,
                                   text="CINEMA MODE",
                                   font='System 14 bold',
                                   bg=self.tool_panel_background_color)
        self.__cinema_mode.pack()
        self.__cinema_mode.place(x=920, y=120)

        self.__cinema_mode_play_image = ImageTk.PhotoImage(
            Image.open("View/Assets/play.png").resize((30, 30), Image.BICUBIC))
        self.__cinema_mode_play_button = Button(self.__root_view,
                                                text="   Start animating ",
                                                image=self.__cinema_mode_play_image,
                                                compound="left",
                                                command=self.start_cinema_mode)
        self.__cinema_mode_play_button.pack()
        self.__cinema_mode_play_button.place(x=930, y=150)

        self.__cinema_mode_stop_image = ImageTk.PhotoImage(
            Image.open("View/Assets/stop.png").resize((30, 30), Image.BICUBIC))
        self.__cinema_mode_stop_button = Button(self.__root_view,
                                                text="   Stop animating ",
                                                image=self.__cinema_mode_stop_image,
                                                compound="left",
                                                command=self.stop_cinema_mode)
        self.__cinema_mode_stop_button.pack()
        self.__cinema_mode_stop_button.place(x=930, y=190)

        # Quality indicators section
        self.__image_quality_indicators = ImageQualityLayout.build_image_quality_title(self.__root_view)

        self.__noise_threshold_selector = ImageQualityLayout.build_image_quality_threshold_label(self.__root_view)
        self.__noise_threshold_selector_value = ImageQualityLayout.build_image_quality_threshold_entry(self.__root_view)
        self.__noise_threshold_selector_value.bind('<Return>', self.threshold_enter_did_change_value)

        self.__image_quality_power_title, self.__image_quality_power_value = ImageQualityLayout.build_image_quality_power(
            self.__root_view)
        self.__image_quality_contrast_title, self.__image_quality_contrast_value = ImageQualityLayout.build_image_quality_contrast(
            self.__root_view)
        self.__image_quality_noise_power_title, self.__image_quality_noise_power_value = ImageQualityLayout.build_image_quality_noise_power(
            self.__root_view)
        self.__image_quality_snr_title, self.__image_quality_snr_value = ImageQualityLayout.build_image_quality_snr(
            self.__root_view)
        self.__image_quality_cnr_title, self.__image_quality_cnr_value = ImageQualityLayout.build_image_quality_cnr(
            self.__root_view)

        # Contrast adjustment section
        self.__contrast_adjustment_title = ContrastAdjustmentLayout.build_contrast_adjustment_title(self.__root_view)

        self.__contrast_adjustment_lower_bound_title = \
            ContrastAdjustmentLayout.build_contrast_selector_subtitle(root_view=self.__root_view,
                                                                      label_title="Lower bound",
                                                                      origin=(920, 520))
        self.__contrast_adjustment_lower_bound_value, self.__contrast_adjustment_lower_bound_slider = \
            ContrastAdjustmentLayout.build_contrast_selector_slider(root_view=self.__root_view,
                                                                    sliding_range=(0, 100),
                                                                    command=self.contrast_sliders_did_change_value,
                                                                    coordinates=(920, 540))

        self.__contrast_adjustment_upper_bound_title = \
            ContrastAdjustmentLayout.build_contrast_selector_subtitle(root_view=self.__root_view,
                                                                      label_title="Upper bound",
                                                                      origin=(920, 590))
        self.__contrast_adjustment_upper_bound_value, self.__contrast_adjustment_upper_bound_slider = \
            ContrastAdjustmentLayout.build_contrast_selector_slider(root_view=self.__root_view,
                                                                    sliding_range=(0, 100),
                                                                    command=self.contrast_sliders_did_change_value,
                                                                    coordinates=(920, 610))

        # ADD SEPARATOR
        self.__tool_frame = Frame(self.__root_view, bg=self.tool_panel_background_color, width=900, height=2)
        self.__tool_frame.place(x=0, y=65)

        # ADD IMAGE CANVAS
        self.__loaded_image_raw = cv2.resize(cv2.imread("View/Assets/waiting.png"),
                                             (875, 610),
                                             interpolation=cv2.INTER_AREA)
        self.__loaded_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.__loaded_image_raw))

        self.__image_view = tk.Canvas(self.__root_view, width=875, height=610)
        self.__loaded_image_view = self.__image_view.create_image(0, 0, image=self.__loaded_image, anchor=tk.NW)
        self.__image_view.image = self.__loaded_image
        self.__image_view.pack()
        self.__image_view.place(x=10, y=75)

    def open_file_dialog(self):
        """
        Opens a file dialog requesting the user the path of the DICOM file to be opened.
        """
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a file",
                                              filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))
        if filename != "":
            self.listener(ListenerCode.DID_PICKED_IMAGE, file=filename)

    def quit(self):
        """
        Stops the execution of the program
        """
        self.__root_view.destroy()

    def load_image_metadata(self):
        """
        Loads the metadata of the image
        """
        self.listener(ListenerCode.SHOW_IMAGE_METADATA)

    @staticmethod
    def show_image_metadata(image_metadata: List[List[str]]):
        """
        Shows the metadata in a new view,

        Args:
            image_metadata: A list, containing lists with the key-value information.
        """
        image_metadata_root_view = tk.Toplevel()
        image_metadata_root_view.resizable(False, False)
        image_metadata_root_view.title("Image metadata")
        _ = ImageMetadataView(image_metadata_root_view, image_metadata)
        image_metadata_root_view.geometry("650x200+10+10")

    def set_image(self, image: numpy.ndarray):
        """
        Shows an image from its array representation in the ImageView, represented as a Canvas object.

        Args:
            image: A numpy array, representing the image.
        """
        self.__loaded_image_raw = cv2.resize(image,
                                             (875, 610),
                                             interpolation=cv2.INTER_AREA)
        self.__loaded_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.__loaded_image_raw))
        self.__image_view.itemconfig(self.__loaded_image_view, image=self.__loaded_image)
        self.__root_view.update()

    def set_image_quality_indicator(self, quality_indicators: ImageQualityIndicators):
        """
        Sets the quality indicator of the image.

        Args:
            quality_indicators: An ImageQualityIndicators object, containing the different indicators.

        """
        if quality_indicators.is_well_defined():
            self.__image_quality_power_value.config(text=str(round(quality_indicators.get_power(), 2)))
            self.__image_quality_contrast_value.config(text=str(round(quality_indicators.get_contrast(), 2)))
            self.__image_quality_noise_power_value.config(text=str(round(quality_indicators.get_noise_power(), 2)))
            self.__image_quality_snr_value.config(text=str(round(quality_indicators.get_signal_noise_ratio(), 2)))
            self.__image_quality_cnr_value.config(text=str(round(quality_indicators.get_contrast_noise_ratio(), 2)))
        else:
            self.__image_quality_power_value.config(text="UNDEF")
            self.__image_quality_contrast_value.config(text="UNDEF")
            self.__image_quality_noise_power_value.config(text="UNDEF")
            self.__image_quality_snr_value.config(text="UNDEF")
            self.__image_quality_cnr_value.config(text="UNDEF")

        self.__root_view.update()

    def initial_view_data(self, z_axis_range: int, contrast_range: Tuple[int, int]):
        """
        Sets the initial data when an image is loaded.

        Args:
            z_axis_range: An integer, representing the range of the Z axis in the DICOM image.
            contrast_range: A Tuple of two elements, containing the range of the sliders.
        """
        self.__show_image_metadata_button.configure(state='active')
        self.__measure_distance_button.configure(state='active')
        self.__zoom_button.configure(state='active')
        #self.__projections_button.configure(state='active')

        self.__radio_button_x_axis.configure(state='active')
        self.__radio_button_y_axis.configure(state='active')
        self.__radio_button_z_axis.configure(state='active')
        self.__radio_button_value.set(2)

        self.set_slider_range(slider=self.slice_slider, sliding_range=(0, z_axis_range))
        self.set_slider_range(slider=self.__contrast_adjustment_lower_bound_slider,
                              sliding_range=contrast_range)
        self.set_slider_range(slider=self.__contrast_adjustment_upper_bound_slider,
                              sliding_range=contrast_range)

        self.__contrast_adjustment_upper_bound_value.set(contrast_range[1])
        self.__contrast_adjustment_lower_bound_value.set(contrast_range[0])

    def set_slider_range(self, slider: tk.Scale, sliding_range: Tuple[int, int]):
        """
        Sets the range of the slider

        Args:
            slider: A tk.Scale object.
            sliding_range: A tuple of two elements, representing the range of the slider.
        """
        slider.configure(from_=sliding_range[0], to=sliding_range[1], state='active')

    def set_slider_value(self, value: int):
        """
        Sets the value of the slider

        Args:
            value: An integer, representing the value of the slider.
        """
        self.__slice_slider_value.set(value)
        self.__root_view.update()

    def radio_button_did_switch(self):
        """
        Detects an event in the radio button group that manages the different perspectives.
        """
        self.__slice_slider_value.set(0)
        self.slice_event()

    def slider_value_did_change(self, _):
        """
        Detects an event in the slider that manages the value of the perspective.
        """
        self.slice_event()

    def slice_event(self):
        """
        Manages the events in the radio buttons and the slider.
        """
        self.listener(ListenerCode.SLICE_VIEW_DID_CHANGE,
                      selected_radio_button=self.__radio_button_value.get(),
                      slider_value=self.__slice_slider_value.get(),
                      noise_threshold=int(self.__noise_threshold_selector_value.get()))

    def start_cinema_mode(self):
        """
        Starts the cinema mode in the viewer.
        """
        noise_threshold = 300
        try:
            noise_threshold = int(self.__noise_threshold_selector_value.get())
        except:
            pass
        self.listener(ListenerCode.CINEMA_MODE_WILL_START,
                      selected_radio_button=self.__radio_button_value.get(),
                      noise_threshold=noise_threshold)

    def stop_cinema_mode(self):
        """
        Stops the cinema mode in the viewer.
        """
        self.listener(ListenerCode.CINEMA_MODE_WILL_STOP)

    def threshold_enter_did_change_value(self, _):
        """
        Detects that the threshold value has changed.
        """
        try:
            value = int(self.__noise_threshold_selector_value.get())
        except:
            value = 300
        self.__noise_threshold_selector_value.delete(0, 'end')
        self.__noise_threshold_selector_value.insert(0, str(value))
        self.listener(ListenerCode.NOISE_THRESHOLD_DID_CHANGE,
                      threshold=int(self.__noise_threshold_selector_value.get()),
                      axis=self.__radio_button_value.get(),
                      slider_value=self.__slice_slider_value.get())

    def contrast_sliders_did_change_value(self, _):
        """
        Detects an event in the sliders that manages the value of the contrast.
        """
        if self.__contrast_adjustment_lower_bound_value.get() > self.__contrast_adjustment_upper_bound_value.get():
            self.__contrast_adjustment_lower_bound_value.set(self.__contrast_adjustment_upper_bound_value.get() - 1)
        self.listener(ListenerCode.CONTRAST_VALUE_DID_CHANGE,
                      contrast_range=(self.__contrast_adjustment_lower_bound_value.get(),
                                        self.__contrast_adjustment_upper_bound_value.get()))

    def show_measure_distance_view(self, pixel_size: Tuple[float, float] = None):
        """
        Shows the measure distance view.

        If pixel_size is not loaded, the controller is called in order to retrieve the distance.

        Args:
            pixel_size: A tuple of two elements, representing the correspondence of 1 pixel in millimeters. Contains
                        the equivalence by rows and by columns.
        """
        if pixel_size is None:
            self.listener(ListenerCode.SHOW_DISTANCE_TOOLS)
        else:
            self.__measure_distance_root_view = tk.Toplevel(self.__root_view)
            self.__measure_distance_root_view.resizable(False, False)
            self.__measure_distance_root_view.title("Measure distance")
            self.__measure_distance_view = MeasureDistanceView(self.__measure_distance_root_view,
                                                               self,
                                                               self.__loaded_image_raw,
                                                               pixel_size)
            self.__measure_distance_root_view.geometry("1180x615+70+70")

    def show_zoom_view(self):
        """
        Shows the zoom view.
        """
        self.__zoom_root_view = tk.Toplevel(self.__root_view)
        self.__zoom_root_view.resizable(False, False)
        self.__zoom_root_view.title("Zoom")
        self.__zoom_view = ZoomView(self.__zoom_root_view,
                                    self.__loaded_image_raw)
        self.__zoom_root_view.geometry("1180x615+70+70")

    def show_projections_view(self):
        """
        Shows the projections view.
        """
        self.__projections_root_view = tk.Toplevel(self.__root_view)
        self.__projections_root_view.resizable(False, False)
        self.__projections_root_view.title("Projections")
        self.__projections_view = ProjectionsView(self.__projections_root_view,
                                                  self.__loaded_image_raw)
        self.__projections_root_view.geometry("1180x615+70+70")


def show_gui(listener: Callable[[ListenerCode, Any], None]) -> Tuple[Tk, MainView]:
    root_view = tk.Tk()
    root_view.resizable(False, False)
    root_view.title('Medical image viewer')
    view = MainView(root_view, listener)
    view.pack(side="top", fill="both", expand=True)
    root_view.geometry("1200x700+10+10")

    return root_view, view
