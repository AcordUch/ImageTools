from enum import Enum
from PIL import Image, ImageDraw

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

    @property
    def width_part(self) -> int | None:
        return self._width_part

    @width_part.setter
    def width_part(self, width_part: int):
        self._width_part = width_part
        self.adjust_to_dividers()
        self.recalculate()
        self.draw_frame()

    @property
    def height_part(self) -> int | None:
        return self._height_part

    @height_part.setter
    def height_part(self, height_part: int):
        self._height_part = height_part
        self.adjust_to_dividers()
        self.recalculate()
        self.draw_frame()

    def load_image(self, path: str) -> None:
        with Image.open(path) as img:
            self.src_image = adjust_to_dividers(img.copy(), self.width_part, self.height_part)
            self.framed_image = self.src_image.copy()
            self.framed_image_canvas = ImageDraw.Draw(self.framed_image, mode="RGBA")

            self.recalculate()
            self.draw_frame()

    def adjust_to_dividers(self):
        if self.src_image == None or self.framed_image == None:
            return

        self.src_image = adjust_to_dividers(self.src_image, self.width_part, self.height_part)
        self.framed_image = adjust_to_dividers(self.src_image, self.width_part, self.height_part)
        self.framed_image_canvas = ImageDraw.Draw(self.framed_image, mode="RGBA")

    def recalculate(self):
        if self.src_image == None or self.framed_image == None:
            return

        frame_width, frame_height = self.src_image.size
        self.image_width = frame_width
        self.image_height = frame_height

        segment_width = int(frame_width / self.width_part)
        segment_height = int(frame_height / self.height_part)
        self.segment_width = segment_width
        self.segment_height = segment_height

    def draw_frame(self) -> None:
        def draw_frame_part(current_width_part: int, current_height_part: int) -> None:
            print(f"draw_frame_part: {current_width_part}, {current_height_part}")

            zero_width = -1 * current_width_part + self.segment_width * current_width_part
            zero_height = -1 * current_height_part + self.segment_height * current_height_part

            end_width = zero_width + self.segment_width - 1
            end_height = zero_height + self.segment_height - 1

            print(f"zero_width: {zero_width}, zero_height: {zero_height}")
            print(f"end_width: {end_width}, end_height: {end_height}")

            self.framed_image_canvas.rectangle(
                ((zero_width, zero_height), (end_width, end_height)),
                outline='red'
            )

        if self.src_image == None or self.framed_image == None:
            return

        for hp in range(self._height_part):
            for wp in range(self._width_part):
                draw_frame_part(wp, hp)
        print("----------")

        self.framed_image.show()


