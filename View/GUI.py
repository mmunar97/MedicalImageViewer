import cv2
import numpy
import threading
import PIL

from Controller.ListenerCode import ListenerCode
from tkinter import *
from tkinter import filedialog
from typing import Any, Callable, List
from PIL import Image, ImageTk

from Model.ImageQualityIndicators import ImageQualityIndicators
from View.GuiBuilder.Layouts.ImageQualityLayout import *
from View.ImageMetadataView import ImageMetadataView


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
        self.__listener = listener

        # BUTTON 1: LOAD IMAGE
        self.__load_image_button_image = ImageTk.PhotoImage(
            Image.open("View/Assets/open_file.png").resize((40, 40), Image.BICUBIC))
        self.__load_image_button = Button(self.__root_view,
                                          text="   Read DICOM image   ",
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
                                                   text="   Show image metadata   ",
                                                   image=self.__show_image_metadata_button_image,
                                                   compound="left",
                                                   command=self.load_image_metadata)
        self.__show_image_metadata_button.pack()
        self.__show_image_metadata_button.place(x=220, y=10)

        # BUTTON 3: EXIT PROGRAM
        self.__exit_button_image = ImageTk.PhotoImage(Image.open("View/Assets/logout.png").resize((40, 40),
                                                                                                  Image.BICUBIC))
        self.__exit_button = Button(self.__root_view,
                                    text="   Exit   ",
                                    image=self.__exit_button_image,
                                    compound="left",
                                    command=self.quit)
        self.__exit_button.pack()
        self.__exit_button.place(x=450, y=10)

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

        self.__slider_value = IntVar()
        self.__slider = Scale(self.__root_view,
                              from_=0, to=42,
                              orient=HORIZONTAL,
                              bg=self.tool_panel_background_color,
                              variable=self.__slider_value,
                              command=self.slider_value_did_change,
                              length=250)
        self.__slider.pack()
        self.__slider.place(x=920, y=65)
        self.__slider.configure(state='disabled')

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

        self.__image_quality_indicators = build_image_quality_title(self.__root_view)

        self.__noise_threshold_selector = build_image_quality_threshold_label(self.__root_view)
        self.__noise_threshold_selector_value = build_image_quality_threshold_entry(self.__root_view)

        self.__image_quality_power_title,  self.__image_quality_power_value = build_image_quality_power(self.__root_view)
        self.__image_quality_contrast_title, self.__image_quality_contrast_value = build_image_quality_contrast(self.__root_view)
        self.__image_quality_noise_power_title, self.__image_quality_noise_power_value = build_image_quality_noise_power(self.__root_view)
        self.__image_quality_snr_title, self.__image_quality_snr_value = build_image_quality_snr(self.__root_view)
        self.__image_quality_cnr_title, self.__image_quality_cnr_value = build_image_quality_cnr(self.__root_view)

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
            self.__listener(ListenerCode.DID_PICKED_IMAGE, file=filename)

    def quit(self):
        """
        Stops the execution of the program
        """
        self.__root_view.destroy()

    def load_image_metadata(self):
        """
        Loads the metadata of the image
        """
        self.__listener(ListenerCode.SHOW_IMAGE_METADATA)

    @staticmethod
    def show_image_metadata(image_metadata: List[List[str]]):
        """
        Shows the metadata in a new view,

        Args:
            image_metadata: A list, containing lists with the key-value information.
        """
        image_metadata_root_view = tk.Tk()
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
        self.__image_quality_power_value.config(text=str(round(quality_indicators.get_power(), 2)))
        self.__image_quality_contrast_value.config(text=str(round(quality_indicators.get_contrast(), 2)))
        self.__image_quality_noise_power_value.config(text=str(round(quality_indicators.get_noise_power(), 2)))
        self.__image_quality_snr_value.config(text=str(round(quality_indicators.get_noise_power(), 2)))
        self.__image_quality_cnr_value.config(text=str(round(quality_indicators.get_noise_power(), 2)))

        self.__root_view.update()

    def initial_view_data(self, z_axis_range: int):
        """
        Sets the initial data when an image is loaded.

        Args:
            z_axis_range: An integer, representing the range of the Z axis in the DICOM image.
        """
        self.__radio_button_x_axis.configure(state='active')
        self.__radio_button_y_axis.configure(state='active')
        self.__radio_button_z_axis.configure(state='active')
        self.__radio_button_value.set(2)

        self.set_slider_range(z_axis_range)

    def set_slider_range(self, range: int):
        """
        Sets the range of the slider

        Args:
            range: An integer, representing the range of the slider.
        """
        self.__slider.configure(from_=0, to=range, state='active')

    def set_slider_value(self, value: int):
        """
        Sets the value of the slider

        Args:
            value: An integer, representing the value of the slider.
        """
        self.__slider_value.set(value)
        self.__root_view.update()

    def radio_button_did_switch(self):
        """
        Detects an event in the radio button group that manages the different perspectives.
        """
        self.__slider_value.set(0)
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
        self.__listener(ListenerCode.SLICE_VIEW_DID_CHANGE,
                        selected_radio_button=self.__radio_button_value.get(),
                        slider_value=self.__slider_value.get(),
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
        self.__listener(ListenerCode.START_CINEMA_MODE,
                        selected_radio_button=self.__radio_button_value.get(),
                        noise_threshold=noise_threshold)

    def stop_cinema_mode(self):
        """
        Stops the cinema mode in the viewer.
        """
        self.__listener(ListenerCode.STOP_CINEMA_MODE)


def show_gui(listener: Callable[[ListenerCode, Any], None]) -> Tuple[Tk, MainView]:
    root_view = tk.Tk()
    root_view.resizable(False, False)
    root_view.title('Medical image viewer')
    view = MainView(root_view, listener)
    view.pack(side="top", fill="both", expand=True)
    root_view.geometry("1200x700+10+10")

    return root_view, view
