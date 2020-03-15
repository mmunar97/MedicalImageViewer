import numpy
import pydicom
import threading
from Controller.ListenerCode import ListenerCode
from typing import Any, Callable, List


class DicomModel(threading.Thread):

    def __init__(self, listener: Callable[[ListenerCode, Any], None]):
        threading.Thread.__init__(self)

        self.__dicom_image = None
        self.__listener = listener

    def load_dicom_image(self, path: str):
        """
        Loads a DICOM image from the selected path.

        Args:
            path: A string, representing the path of the selected file.
        """
        self.__dicom_image = pydicom.dcmread(path)
        self.__listener(ListenerCode.DID_LOAD_IMAGE,
                        image=self.__dicom_image.pixel_array[:, :, 0],
                        z_axis_range=self.get_range(2))

    def get_slice_image(self, axis: int, index: int) -> numpy.ndarray:
        """
        Returns the slide image in an axis with a certain index.

        Args:
            axis: An integer, representing the axis.
            index: An integer, representing the index of the image in the axis.

        Returns:
            An image, represented as a numpy array.
        """
        if axis == 0:
            return self.__dicom_image.pixel_array[index, :, :]
        elif axis == 1:
            return self.__dicom_image.pixel_array[:, index, :]
        elif axis == 2:
            return self.__dicom_image.pixel_array[:, :, index]

    def get_range(self, axis: int):
        """
        Returns the range of the DICOM file in a certain axis.

        Args:
            axis: An intener, representing the axis.

        Returns:
            An integer, representing the range of the DICOM file in a certain axis.
        """
        return self.__dicom_image.pixel_array.shape[axis]-1

    def get_file_metadata(self) -> List[List[str]]:
        """
        Returns the metadata of the loaded file

        Returns: A list, containing lists with the key-value information.
        """
        def retrieve_metadata(dataset):
            data = []
            skip_print = ['Pixel Data', 'File Meta Information Version']
            for data_element in dataset:
                if data_element.VR == "SQ":
                    for sequence_item in data_element.value:
                        data = data + retrieve_metadata(sequence_item)
                else:
                    if data_element.name not in skip_print:
                        repr_value = repr(data_element.value)
                        if len(repr_value) > 50:
                            repr_value = repr_value[:50] + "..."
                        data.append([data_element.name, repr_value])
            return data

        if self.__dicom_image is not None:
            return retrieve_metadata(dataset=self.__dicom_image)
        else:
            return None


