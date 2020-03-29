import atexit
from Controller.ListenerCode import ListenerCode
from Model.DicomModel import DicomModel
from Model.ImageQualityIndicators import compute_quality_indicators
from Model.Logger.LogEntry import LogEntry
from Model.Logger.LogManager import LogManager
from View.GUI import show_gui


class MedicalImageViewer:

    def __init__(self):
        """
        Initializes the object that manages the events in the execution.
        """
        self.__model = DicomModel(self.medical_image_listener)
        self.__model.start()

        self.__log_manager = LogManager()
        self.__log_manager.start()

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

            self.__log_manager.append_new_log(LogEntry("DID_PICKED_IMAGE",
                                                       "NEW IMAGE PICKED FROM PATH " + file_path))

        elif action_code == ListenerCode.DID_LOAD_IMAGE:
            image = kwargs['image']
            z_axis_range = kwargs['z_axis_range']
            contrast_range = kwargs['contrast_range']
            self.__view.set_image(image)
            self.__view.initial_view_data(z_axis_range=z_axis_range, contrast_range=contrast_range)

            self.__log_manager.append_new_log(LogEntry("DID_LOAD_IMAGE",
                                                       "IMAGE WAS LOAD SUCCESSFULLY"))
            self.__log_manager.append_new_log(LogEntry("DID_REFRESH_VIEW",
                                                       "Z AXIS RANGE WAS SET: " + str(z_axis_range)))
            self.__log_manager.append_new_log(LogEntry("DID_REFRESH_VIEW",
                                                       "CONTRAST RANGE WAS SET: " + str(contrast_range)))

        elif action_code == ListenerCode.SLICE_VIEW_DID_CHANGE:
            selected_radio_button, slider_value, noise_threshold = kwargs['selected_radio_button'], kwargs[
                'slider_value'], kwargs['noise_threshold']
            image = self.__model.get_slice_image(selected_radio_button, slider_value)
            image_range = self.__model.get_range(selected_radio_button)
            self.__view.set_image_quality_indicator(
                compute_quality_indicators(image.astype('float64'), noise_threshold))

            self.__view.set_image(image)
            self.__view.set_slider_range(self.__view.slice_slider, (0, image_range))

            self.__log_manager.append_new_log(LogEntry("SLIDER_AXIS_CHANGED",
                                                       "SELECTED AXIS: " + str(selected_radio_button) +
                                                       "\t WITH SLIDER VALUE: " + str(slider_value) +
                                                       "\t WITH NOISE THRESHOLD" + str(noise_threshold)))

        elif action_code == ListenerCode.SHOW_IMAGE_METADATA:
            metadata = self.__model.get_file_metadata()
            if metadata is not None:
                self.__view.show_image_metadata(metadata)
                self.__log_manager.append_new_log(LogEntry("DID_SHOW_METADATA",
                                                           "METADATA WINDOW WAS SHOWN"))
        elif action_code == ListenerCode.CINEMA_MODE_WILL_START:
            selected_radio_button = kwargs['selected_radio_button']
            noise_threshold = kwargs['noise_threshold']
            self.__model.start_cinema_mode(selected_radio_button,
                                           noise_threshold)

            self.__log_manager.append_new_log(LogEntry("CINEMA_MODE_DID_START",
                                                       "CINEMA MODE HAS STARTED WITH PARAMETERS: " +
                                                       "SELECTED AXIS: " + str(selected_radio_button) + "\t" +
                                                       "NOISE THRESHOLD" + str(noise_threshold)))

        elif action_code == ListenerCode.CINEMA_MODE_WILL_STOP:
            self.__model.stop_cinema_mode()
            self.__log_manager.append_new_log(LogEntry("CINEMA_MODE_DID_STOP",
                                                       "CINEMA MODE HAS STOPPED"))

        elif action_code == ListenerCode.PRINT_IMAGE_SLICE:
            image = kwargs['image']
            index = kwargs['index']
            quality_image = kwargs['quality_indicator']

            self.__view.set_image(image)
            self.__view.set_slider_value(index)
            self.__view.set_image_quality_indicator(quality_image)

            self.__log_manager.append_new_log(LogEntry("DID_REFRESH_VIEW",
                                                       "THE IMAGE WAS CHANGED"))

        elif action_code == ListenerCode.NOISE_THRESHOLD_DID_CHANGE:
            threshold = kwargs['threshold']
            axis = kwargs['axis']
            slider_value = kwargs['slider_value']

            quality_indicator = self.__model.show_quality_indicators(axis, slider_value, threshold)
            if quality_indicator is not None:
                self.__view.set_image_quality_indicator(quality_indicator)

                self.__log_manager.append_new_log(LogEntry("THRESHOLD_DID_CHANGE",
                                                           "THE THRESHOLD WAS CHANGED: "+str(threshold)))

        elif action_code == ListenerCode.CONTRAST_VALUE_DID_CHANGE:
            contrast_range = kwargs['contrast_range']
            self.__model.set_contrast_range(contrast_range)

            self.__log_manager.append_new_log(LogEntry("CONTRAST_DID_CHANGE",
                                                       "THE CONTRAST WAS CHANGED: "+str(contrast_range)))

        elif action_code == ListenerCode.SHOW_DISTANCE_TOOLS:
            pixel_size = self.__model.get_pixel_values()

            self.__view.show_measure_distance_view(pixel_size)

            self.__log_manager.append_new_log(LogEntry("DISTANCE_TOOLS_SHOWN",
                                                       "THE TOOLS WINDOW IS SHOWN"))

        elif action_code == ListenerCode.POINT_DISTANCE_DID_CHANGE:

            self.__log_manager.append_new_log(LogEntry("DISTANCE_ENTRY_CHANGED",
                                                       "SELECTED POINTS CHANGED IN THE DISTANCE ENTRY: " +
                                                       "POINT 1="+str(kwargs['point1'])+"\t" +
                                                       "POINT 2="+str(kwargs['point2'])))
