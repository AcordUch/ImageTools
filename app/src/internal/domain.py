import logging
from io import BytesIO
from typing import Tuple, List

from PIL import Image, ImageDraw
from kivy.core.image import Image as CoreImage

from common.src.domain.domain import CropType


class CropFrame:
    def __init__(self):
        self._src_image: Image.Image | None = None
        self.framed_image: Image.Image | None = None
        self.framed_image_canvas: ImageDraw.ImageDraw | None = None
        self.crop_type: CropType = CropType.SQUARE
        self._width_part: int = 1
        self._height_part: int = 1
        self._segment_width: int = 0
        self._segment_height: int = 0
        self._frame_width: int = 0
        self._frame_height: int = 0
        self._frame_zero_x: int = 0
        self._frame_zero_y: int = 0
        self._image_center_x: int = 0
        self._image_center_y: int = 0
        self._frames: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    @property
    def src_image(self) -> Image.Image | None:
        return self._src_image

    def load_image(self, path: str) -> None:
        with Image.open(path) as img:
            self._src_image = img.copy()

        self._reinitialize_canvas()
        self._recalculate_from_image()
        self._crop_to_frame()

    @property
    def width_part(self) -> int | None:
        return self._width_part

    @width_part.setter
    def width_part(self, width_part: int):
        logging.debug(f"Set: width_part={width_part}")

        increase = width_part > self._width_part

        self._width_part = width_part

        self._reinitialize_canvas()

        self._adjust_frame_to_dividers(increase)
        self._recalculate_from_frame()

        if self.crop_type == CropType.SQUARE:
            self._segment_to_square_width()
            self._recalculate_frame_height()
        self._recalculate_frame_width()

        is_clamped = self._clamp_to_screen()
        if is_clamped:
            self._adjust_frame_to_dividers(False)
            self._recalculate_from_frame()

        self._frame_x_y_from_center()
        self._crop_to_frame()

    @property
    def height_part(self) -> int | None:
        return self._height_part

    @height_part.setter
    def height_part(self, height_part: int):
        logging.debug(f"Set: height_part={height_part}")

        increase = height_part > self._height_part

        self._height_part = height_part

        self._reinitialize_canvas()

        self._adjust_frame_to_dividers(increase)
        self._recalculate_from_frame()

        if self.crop_type == CropType.SQUARE:
            self._segment_to_square_height()
            self._recalculate_frame_width()
        self._recalculate_frame_height()

        is_clamped = self._clamp_to_screen()
        if is_clamped:
            self._adjust_frame_to_dividers(False)
            self._recalculate_from_frame()

        self._frame_x_y_from_center()
        self._crop_to_frame()

    @property
    def segment_width(self) -> int | None:
        return self._segment_width

    @segment_width.setter
    def segment_width(self, segment_width: int) -> None:
        logging.debug(f"Set: segment_width={segment_width}")

        if segment_width < 1:
            return

        if self.crop_type == CropType.SQUARE:
            self._segment_square_mod(segment_width - self._segment_width)
            return

        self._segment_width = segment_width

        self._reinitialize_canvas()
        self._recalculate_frame_width()
        self._crop_to_frame()

    @property
    def segment_height(self) -> int | None:
        return self._segment_height

    @segment_height.setter
    def segment_height(self, segment_height: int) -> None:
        logging.debug(f"Set: segment_height={segment_height}")

        if segment_height < 1:
            return

        if self.crop_type == CropType.SQUARE:
            self._segment_square_mod(segment_height - self._segment_height)
            return

        self._segment_height = segment_height

        self._reinitialize_canvas()
        self._recalculate_frame_height()
        self._crop_to_frame()

    def _segment_square_mod(self, delta: int) -> None:
        self._segment_width += delta
        self._segment_height += delta

        self._reinitialize_canvas()
        self._recalculate_frame_width()
        self._recalculate_frame_height()
        self._crop_to_frame()

    def _segment_to_square_width(self) -> None:
        self._segment_width = self.segment_width
        self._segment_height = self.segment_width

    def _segment_to_square_height(self) -> None:
        self._segment_width = self.segment_height
        self._segment_height = self.segment_height

    @property
    def frame_zero_x(self) -> int | None:
        return self._frame_zero_x

    @frame_zero_x.setter
    def frame_zero_x(self, frame_zero_x: int) -> None:
        logging.debug(f"Set: frame_zero_x={frame_zero_x}")

        self._frame_zero_x = frame_zero_x

        self._reinitialize_canvas()
        self._crop_to_frame()

    @property
    def frame_zero_y(self) -> int | None:
        return self._frame_zero_y

    @frame_zero_y.setter
    def frame_zero_y(self, frame_zero_y: int) -> None:
        logging.debug(f"Set: frame_zero_y={frame_zero_y}")

        self._frame_zero_y = frame_zero_y

        self._reinitialize_canvas()
        self._crop_to_frame()

    @property
    def frames(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return self._frames

    def _frame_x_y_from_center(self) -> None:
        self._frame_zero_x = self._image_center_x - self._frame_width // 2
        self._frame_zero_y = self._image_center_y - self._frame_height // 2

    def _frame_to_square(self) -> None:
        min_size = min(self._frame_width, self._frame_height)
        self._frame_width = min_size
        self._frame_height = min_size

    def _adjust_frame_to_dividers(self, increase: bool) -> None:
        logging.debug(f"Call: adjust_image_to_dividers")

        width_div = self._frame_width % self.width_part
        height_div = self._frame_height % self.height_part

        if width_div != 0:
            self._frame_width = self._frame_width + self.width_part - width_div if increase else self._frame_width - width_div

        if height_div != 0:
            self._frame_height = self._frame_height + self.height_part - height_div if increase else self._frame_height - height_div

    def _reinitialize_canvas(self) -> None:
        logging.debug(f"Call: reinitialize_canvas")

        if self._src_image == None:
            logging.debug(f"Self.src_image is None")
            return

        self.framed_image = self._src_image.copy()
        self.framed_image_canvas = ImageDraw.Draw(self.framed_image, mode="RGBA")

    def _recalculate_from_image(self) -> None:
        logging.debug(f"Call: recalculate_from_image")

        if self._src_image == None:
            logging.debug(f"Self.src_image is None")
            return

        img_width, img_height = self._src_image.size

        self._image_center_x, self._image_center_y = img_width // 2, img_height // 2
        self._frame_width, self._frame_height = img_width - 2, img_height - 2

        self._frame_to_square()
        self._frame_x_y_from_center()

        self._segment_width = int(self._frame_width / self.width_part)
        self._segment_height = int(self._frame_height / self.height_part)

    def _recalculate_from_frame(self) -> None:
        logging.debug(f"Call: recalculate_from_frame")

        self._segment_width = int(self._frame_width / self.width_part)
        self._segment_height = int(self._frame_height / self.height_part)

    def _recalculate_frame_width(self) -> None:
        logging.debug(f"Call: recalculate_frame_width")

        self._frame_width = self.segment_width * self.width_part

    def _recalculate_frame_height(self) -> None:
        logging.debug(f"Call: recalculate_frame_height")

        self._frame_height = self.segment_height * self.height_part

    def _clamp_to_screen(self) -> bool:
        logging.debug(f"Call: clamp_to_screen")

        if self._src_image is None:
            logging.debug(f"Self.src_image is None")
            return False

        img_width, img_height = self._src_image.size
        is_clamped = False

        if self._frame_width >= img_width:
            self._frame_width = img_width - 2
            is_clamped = True

        if self._frame_height >= img_height:
            self._frame_height = img_height - 2
            is_clamped = True

        return is_clamped

    def _crop_to_frame(self) -> None:
        def _crop_to_frame_part(current_width_part: int, current_height_part: int) -> None:
            zero_width = self.frame_zero_x + self.segment_width * current_width_part
            zero_height = self.frame_zero_y + self.segment_height * current_height_part

            end_width = zero_width + self.segment_width
            end_height = zero_height + self.segment_height

            self._frames.append(((zero_width, zero_height), (end_width, end_height)))

        logging.debug(f"Call: crop_to_frame")

        self._frames = []

        for hp in range(self._height_part):
            for wp in range(self._width_part):
                _crop_to_frame_part(wp, hp)

        logging.debug(f"Result: self._frames: {self._frames}")

    def draw_frame(self) -> None:
        logging.debug(f"Call: draw_frame")

        if self.framed_image_canvas is None:
            logging.debug(f"Self.framed_image_canvas is None")
            return

        for frame in self._frames:
            self.framed_image_canvas.rectangle(frame, outline='red')

    def generate_kivy_image(self) -> CoreImage | None:
        logging.debug(f"Call: draw_frame")

        if self.framed_image_canvas is None:
            logging.debug(f"Self.framed_image_canvas is None")
            return None

        self.draw_frame()

        memory_file = BytesIO()
        self.framed_image.save(memory_file, format='png')
        memory_file.seek(0)

        return CoreImage(memory_file, ext='png')

    def crop_image(self) -> List[Image.Image]:
        logging.debug(f"Call: crop_image")

        if self._src_image is None:
            logging.debug(f"Self.src_image is None")
            return []

        list_of_cropped_images: List[Image.Image] = []

        for frame in self._frames:
            tmp_img = self._src_image.copy()
            list_of_cropped_images.append(tmp_img.crop((frame[0][0], frame[0][1], frame[1][0], frame[1][1])))

        return list_of_cropped_images
