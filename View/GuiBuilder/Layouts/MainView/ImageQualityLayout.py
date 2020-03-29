from View.GuiBuilder.Base import *
from View.GuiBuilder.Values.Colors import Colors
from View.GuiBuilder.Values.Fonts import Fonts


def build_image_quality_title(root_view: tk.Tk) -> tk.Label:
    """
    Builds the title in the image quality region.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tk.Label object.
    """
    return build_label(root_view=root_view,
                       text="IMAGE QUALITY INDICATORS",
                       font=Fonts.BOLD.value,
                       background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                       coordinates=(920, 250))


def build_image_quality_threshold_label(root_view: tk.Tk) -> tk.Label:
    """
    Builds the label as indicator of the noise threshold selector.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tk.Label object.
    """
    return build_label(root_view=root_view,
                       text="Noise threshold",
                       font=Fonts.REGULAR.value,
                       background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                       coordinates=(920, 280))


def build_image_quality_threshold_entry(root_view: tk.Tk) -> tk.Entry:
    """
    Builds the entry that contains the threshold to be used as noise limit.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tk.Entry object.
    """
    return build_edit_text(root_view=root_view,
                           placeholder="300",
                           coordinates=(1040, 280),
                           size=(100, 30))


def build_image_quality_power(root_view: tk.Tk) -> Tuple[tk.Label, tk.Label]:
    """
    Builds the signal power labels that contains the title and the value.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tuple of two tk.Label objects.
    """
    power_label = build_label(root_view=root_view,
                              text="Signal power",
                              font=Fonts.REGULAR.value,
                              background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                              coordinates=(920, 330))
    power_label_value = build_label(root_view=root_view,
                                    text="-----------",
                                    font=Fonts.REGULAR.value,
                                    background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                                    coordinates=(1040, 330))
    return power_label, power_label_value


def build_image_quality_contrast(root_view: tk.Tk) -> Tuple[tk.Label, tk.Label]:
    """
    Builds the contrast labels that contains the title and the value.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tuple of two tk.Label objects.
    """
    contrast_label = build_label(root_view=root_view,
                                 text="Contrast",
                                 font=Fonts.REGULAR.value,
                                 background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                                 coordinates=(920, 360))
    contrast_label_value = build_label(root_view=root_view,
                                       text="-----------",
                                       font=Fonts.REGULAR.value,
                                       background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                                       coordinates=(1040, 360))
    return contrast_label, contrast_label_value


def build_image_quality_noise_power(root_view: tk.Tk) -> Tuple[tk.Label, tk.Label]:
    """
    Builds the noise power labels that contains the title and the value.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tuple of two tk.Label objects.
    """
    noise_power_label = build_label(root_view=root_view,
                                    text="Noise power",
                                    font=Fonts.REGULAR.value,
                                    background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                                    coordinates=(920, 390))
    noise_power_value = build_label(root_view=root_view,
                                    text="-----------",
                                    font=Fonts.REGULAR.value,
                                    background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                                    coordinates=(1040, 390))
    return noise_power_label, noise_power_value


def build_image_quality_snr(root_view: tk.Tk) -> Tuple[tk.Label, tk.Label]:
    """
    Builds the SNR labels that contains the title and the value.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tuple of two tk.Label objects.
    """
    snr_label = build_label(root_view=root_view,
                            text="SNR",
                            font=Fonts.REGULAR.value,
                            background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                            coordinates=(920, 420))
    snr_value = build_label(root_view=root_view,
                            text="-----------",
                            font=Fonts.REGULAR.value,
                            background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                            coordinates=(1040, 420))
    return snr_label, snr_value


def build_image_quality_cnr(root_view: tk.Tk) -> Tuple[tk.Label, tk.Label]:
    """
    Builds the CNR labels that contains the title and the value.

    Args:
        root_view: The root view of the layout.

    Returns:
        A tuple of two tk.Label objects.
    """
    cnr_label = build_label(root_view=root_view,
                            text="CNR",
                            font=Fonts.REGULAR.value,
                            background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                            coordinates=(920, 450))
    cnr_value = build_label(root_view=root_view,
                            text="-----------",
                            font=Fonts.REGULAR.value,
                            background_color=Colors.TOOLS_PANEL_BACKGROUND.value,
                            coordinates=(1040, 450))
    return cnr_label, cnr_value
