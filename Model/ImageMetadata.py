from typing import Tuple


class ImageMetadata:

    def __init__(self, shape: Tuple[int, int, int]):
        self.shape_x = shape[0]
        self.shape_y = shape[1]
        self.shape_z = shape[2]
