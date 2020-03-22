from Controller.ListenerCode import ListenerCode
from Model.DicomModel import DicomModel
from Model.ImageQualityIndicators import compute_quality_indicators
from View.GUI import show_gui


class MedicalImageViewer:

    def __init__(self):
        """
        Initializes the object that manages the events in the execution.
        """
        self.__model = DicomModel(self.medical_image_listener)
        self.__model.start()

        self.__root_view, self.__view = show_gui(self.medical_image_listener)
        self.__view.start()
        self.__view.mainloop()
        self.__root_view.mainloop()

    def medical_image_listener(self, action_code: ListenerCode, **kwargs):
        """
        Listener of the different events that occur in the GUI or in the model.

        Args:
            action_code: A ListenerCode value, representing the action to handle.
            **kwargs: Arguments of the action.
        """
        if action_code == ListenerCode.DID_PICKED_IMAGE:
            file_path = kwargs['file']
            self.__model.load_dicom_image(file_path)
        elif action_code == ListenerCode.DID_LOAD_IMAGE:
            image = kwargs['image']
            z_axis_range = kwargs['z_axis_range']
            self.__view.set_image(image)
            self.__view.initial_view_data(z_axis_range=z_axis_range)
        elif action_code == ListenerCode.SLICE_VIEW_DID_CHANGE:
            selected_radio_button, slider_value, noise_threshold = kwargs['selected_radio_button'], kwargs['slider_value'], kwargs['noise_threshold']
            image = self.__model.get_slice_image(selected_radio_button, slider_value)
            image_range = self.__model.get_range(selected_radio_button)
            self.__view.set_image_quality_indicator(compute_quality_indicators(image.astype('float64'),
                                                                               noise_threshold))

            self.__view.set_image(image)
            self.__view.set_slider_range(image_range)
        elif action_code == ListenerCode.SHOW_IMAGE_METADATA:
            metadata = self.__model.get_file_metadata()
            if metadata is not None:
                self.__view.show_image_metadata(metadata)
        elif action_code == ListenerCode.START_CINEMA_MODE:
            selected_radio_button = kwargs['selected_radio_button']
            noise_threshold = kwargs['noise_threshold']
            self.__model.start_cinema_mode(selected_radio_button,
                                           noise_threshold)
        elif action_code == ListenerCode.STOP_CINEMA_MODE:
            self.__model.stop_cinema_mode()
        elif action_code == ListenerCode.PRINT_IMAGE_SLICE:
            image = kwargs['image']
            index = kwargs['index']
            quality_image = kwargs['quality_indicator']

            self.__view.set_image(image)
            self.__view.set_slider_value(index)
            self.__view.set_image_quality_indicator(quality_image)

