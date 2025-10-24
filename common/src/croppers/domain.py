import logging
from enum import Enum
from io import BytesIO
from typing import Tuple, List

from PIL import Image, ImageDraw
from kivy.core.image import Image as CoreImage

from common.src.resizers.original import adjust_to_dividers


class CropType(Enum):
    SQUARE = 0
    WIDTH = 1
    HEIGHT = 2


class CropFrame:
    def __init__(self):
        self.src_image: Image.Image | None = None
        self.framed_image: Image.Image | None = None
        self.framed_image_canvas: ImageDraw.ImageDraw | None = None
        self.crop_type = CropType.SQUARE
        self._width_part = 1
        self._height_part = 1
        self.image_width = 0
        self.image_height = 0
        self.segment_width = 0
        self.segment_height = 0
        self._frames: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    @property
    def width_part(self) -> int | None:
        return self._width_part

    @width_part.setter
    def width_part(self, width_part: int):
        logging.debug(f"Set width_part={width_part}")

        self._width_part = width_part

        self.adjust_image_to_dividers()
        self.reinitialize_canvas()
        self.recalculate()
        self.crop_to_frame()

    @property
    def height_part(self) -> int | None:
        return self._height_part

    @height_part.setter
    def height_part(self, height_part: int):
        logging.debug(f"Set height_part={height_part}")

        self._height_part = height_part

        self.adjust_image_to_dividers()
        self.reinitialize_canvas()
        self.recalculate()
        self.crop_to_frame()

    @property
    def frames(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return self._frames

    def load_image(self, path: str) -> None:
        with Image.open(path) as img:
            self.src_image = img.copy()

        self.adjust_image_to_dividers()
        self.reinitialize_canvas()
        self.recalculate()
        self.crop_to_frame()

    def adjust_image_to_dividers(self):
        logging.debug(f"Call adjust_image_to_dividers")

        if self.src_image == None:
            logging.debug(f"Self.src_image is None")
            return

        self.src_image = adjust_to_dividers(self.src_image, self.width_part, self.height_part)

    def reinitialize_canvas(self):
        logging.debug(f"Call reinitialize_canvas")

        if self.src_image == None:
            logging.debug(f"Self.src_image is None")
            return

        self.framed_image = self.src_image.copy()
        self.framed_image_canvas = ImageDraw.Draw(self.framed_image, mode="RGBA")

    def recalculate(self):
        logging.debug(f"Call recalculate")

        if self.src_image == None:
            logging.debug(f"Self.src_image is None")
            return

        frame_width, frame_height = self.src_image.size
        self.image_width = frame_width
        self.image_height = frame_height

        segment_width = int(frame_width / self.width_part)
        segment_height = int(frame_height / self.height_part)
        self.segment_width = segment_width
        self.segment_height = segment_height

    def crop_to_frame(self) -> None:
        def crop_to_frame_part(current_width_part: int, current_height_part: int) -> None:
            zero_width = -1 * current_width_part + self.segment_width * current_width_part
            zero_height = -1 * current_height_part + self.segment_height * current_height_part

            end_width = zero_width + self.segment_width - 1
            end_height = zero_height + self.segment_height - 1

            self._frames.append(((zero_width, zero_height), (end_width, end_height)))

        logging.debug(f"Call crop_to_frame")

        self._frames = []

        for hp in range(self._height_part):
            for wp in range(self._width_part):
                crop_to_frame_part(wp, hp)

        logging.debug(f"Result self._frames: {self._frames}")

    def draw_frame(self) -> None:
        logging.debug(f"Call draw_frame")

        if self.framed_image_canvas is None:
            logging.debug(f"Self.framed_image_canvas is None")
            return

        for frame in self._frames:
            self.framed_image_canvas.rectangle(frame, outline='red')

    def generate_kivy_image(self) -> CoreImage | None:
        logging.debug(f"Call draw_frame")

        if self.framed_image_canvas is None:
            logging.debug(f"Self.framed_image_canvas is None")
            return None

        self.draw_frame()

        memory_file = BytesIO()
        self.framed_image.save(memory_file, format='png')
        memory_file.seek(0)

        return CoreImage(memory_file, ext='png')

    def crop_image(self) -> List[Image.Image]:
        logging.debug(f"Call crop_image")

        if self.src_image is None:
            logging.debug(f"Self.src_image is None")
            return []

        list_of_cropped_images: List[Image.Image] = []

        for frame in self._frames:
            tmp_img = self.src_image.copy()
            list_of_cropped_images.append(tmp_img.crop((frame[0][0], frame[0][1], frame[1][0], frame[1][1])))

        return list_of_cropped_images
