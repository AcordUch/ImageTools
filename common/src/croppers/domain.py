from enum import Enum
from PIL import Image


class CropType(Enum):
    SQUARE = 0
    WIDTH = 1
    HEIGHT = 2


class CropFrame:
    def __init__(self):
        self._image = None
        self._crop_type = None
        self._width_part = None
        self._height_part = None
        self.frame_width = 0
        self.frame_height = 0
        self.crop_part_width = 0
        self.crop_part_height = 0

    def pre_init(self, image_path: str):
        with Image.open(image_path) as img:
            self._image = img.copy()

    @property
    def crop_type(self) -> CropType | None:
        return self._crop_type

    @crop_type.setter
    def crop_type(self, crop_type: CropType):
        self._crop_type = crop_type

    @property
    def width_part(self) -> int | None:
        return self._width_part

    @width_part.setter
    def width_part(self, width_part: int):
        self._width_part = width_part

    @property
    def height_part(self) -> int | None:
        return self._height_part

    @height_part.setter
    def height_part(self, height_part: int):
        self._height_part = height_part

    def recalculate_width_and_height(self):
        if self._width_part is None or self._height_part is None:
            return

        frame_width, frame_height = self._image.size
        self.frame_width = frame_width
        self.frame_height = frame_height

        crop_part_width = int(frame_width / self._width_part)
        crop_part_height = int(frame_height / self._height_part)
        self.crop_part_width = crop_part_width
        self.crop_part_height = crop_part_height


    # def pre_init(self, crop_img: Image.Image, width_parts: int, height_parts: int):
    #     frame_width, frame_height = crop_img.size
    #     self.frame_width = frame_width
    #     self.frame_height = frame_height
    #
    #     crop_part_width = int(frame_width / width_parts)
    #     crop_part_height = int(frame_height / height_parts)
    #     self.crop_part_width = crop_part_width
    #     self.crop_part_height = crop_part_height
