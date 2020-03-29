import numpy


class ImageQualityIndicators:

    def __init__(self,
                 well_defined: bool,
                 power: float,
                 contrast: float,
                 noise_power: float,
                 snr: float,
                 cnr: float):
        """
        Initializes the object that stores the indicators of quality of a medical image.

        Args:
            well_defined: A boolean, indicating if the indicator is well defined using the threshold.
            power: The power of the signal.
            contrast: The contrast of the signal.
            noise_power: The power of the noise present in the image.
            snr: The Signal-to-Noise ratio of the image.
            cnr: The Contrast-to-Noise ratio of the image.
        """
        self.__well_defined = well_defined
        self.__power = power
        self.__contrast = contrast
        self.__noise_power = noise_power
        self.__snr = snr
        self.__cnr = cnr

    def is_well_defined(self) -> bool:
        """
        Gets if the indicators are well defined using the selected threshold level.

        Returns:
            A boolean, indicating if the indicators are well defined.
        """
        return self.__well_defined

    def get_power(self) -> float:
        """
        Gets the signal power.

        Returns: A float value, representing the power of the signal.
        """
        return self.__power

    def get_contrast(self) -> float:
        """
        Gets the contrast of the signal.

        Returns: A float value, representing the contrast of the signal.
        """
        return self.__contrast

    def get_noise_power(self) -> float:
        """
        Gets the noise power present in the image.

        Returns: A float value, representing the noise power of the signal.
        """
        return self.__noise_power

    def get_signal_noise_ratio(self) -> float:
        """
        Gets the Signal-to-Noise ratio of the image.

        Returns: A float value, representing the Signal-to-Noise ratio of the image.
        """
        return self.__snr

    def get_contrast_noise_ratio(self) -> float:
        """
        gets the Contrast-to-Noise ratio of the image.


        Returns: A float value, representing the Contrast-to-Noise ratio of the image.
        """
        return self.__cnr


def compute_quality_indicators(image: numpy.ndarray, noise_threshold: int) -> ImageQualityIndicators:
    """
    Computes the quality indicators of the image.

    Args:
        image: One slice of a three-dimensional medical image, represented as a numpy ndarray.
        noise_threshold: An integer, representing the threshold for which the pixels are considered as noise.

    Returns:
        An ImageQualityIndicators object, containing the different quality indicators of the image.
    """
    try:
        noise_power = compute_noise_power(image, noise_threshold)
        signal_power = compute_signal_power(image, noise_threshold)
        signal_contrast = compute_signal_contrast(image, noise_threshold)
        snr = compute_signal_noise_ratio(signal_power, noise_power)
        cnr = compute_contrast_noise_ratio(signal_contrast, noise_power)

        return ImageQualityIndicators(True, signal_power, signal_contrast, noise_power, snr, cnr)
    except:
        return ImageQualityIndicators(False, 0, 0, 0, 0, 0)


def compute_noise_power(image: numpy.ndarray, noise_threshold: int) -> float:
    """
    Computes the noise power of the image.

    Args:
        image: One slice of a three-dimensional medical image, represented as a numpy ndarray.
        noise_threshold: An integer, representing the threshold for which the pixels are considered as noise.

    Returns:
        A float value, representing the noise power.
    """
    noise_mask = (image < noise_threshold) * (image > 0)
    return numpy.average(numpy.square(image[noise_mask]))


def compute_signal_power(image: numpy.ndarray, noise_threshold: int) -> float:
    """
    Computes the signal power of the image.

    Args:
        image: One slice of a three-dimensional medical image, represented as a numpy ndarray.
        noise_threshold: An integer, representing the threshold for which the pixels are considered as noise.

    Returns:
        A float value, representing the signal power.
    """
    signal_mask = image > noise_threshold
    return numpy.average(numpy.square(image[signal_mask]))


def compute_signal_contrast(image: numpy.ndarray, noise_threshold: int) -> float:
    """
    Computes the signal contrast of the image.

    Args:
        image: One slice of a three-dimensional medical image, represented as a numpy ndarray.
        noise_threshold: An integer, representing the threshold for which the pixels are considered as noise.

    Returns:
        A float value, representing the contrast of the image.
    """
    signal_mask = image > noise_threshold
    return numpy.max(image[signal_mask] - numpy.min(image[signal_mask]))


def compute_signal_noise_ratio(signal_power: float, noise_power: float) -> float:
    """
    Computes the Signal-to-Noise ratio of the image.

    Args:
        signal_power: The signal power of the image.
        noise_power: The noise power of the image.

    Returns:
        A float value, representing the signal-to-noise ratio of the image.
    """
    return numpy.sqrt(signal_power / noise_power)


def compute_contrast_noise_ratio(signal_contrast: float, noise_power: float) -> float:
    """
    Computes the Contrast-to-Noise ratio of the image.

    Args:
        signal_contrast: The signal contrast of the image.
        noise_power: The noise power of the image.

    Returns:
        A float value, representing the contrast-to-noise ratio of the image.
    """
    return signal_contrast / numpy.sqrt(noise_power)
