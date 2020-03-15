from enum import Enum


class ListenerCode(Enum):
    DID_PICKED_IMAGE = 0
    DID_LOAD_IMAGE = 1
    REFRESH_VIEW_IMAGE_METADATA = 2
    SLICE_VIEW_DID_CHANGE = 3
    SHOW_IMAGE_METADATA = 4

