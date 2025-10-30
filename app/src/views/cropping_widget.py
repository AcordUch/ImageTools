from typing import List, Mapping
from PIL import Image
from collections.abc import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock, ClockEvent

from internal.domain import CropFrame
from common.src.croppers.domain import CropType
from common.src.resizers.domain import ImageTransform
from common.src.resizers.cropped import resize_to_thumbnail

type ResizeFunction = Callable[[int], None]


class CroppingWidget(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    image_texture_property = ObjectProperty(None)

    _crop_frame: CropFrame = ObjectProperty(CropFrame())
    _active_clocks: Mapping[str, List[ClockEvent]] = {}

    def __init__(self, **kwargs):
        super(CroppingWidget, self).__init__(**kwargs)

        self.image_transformers: List[ImageTransform] = [
            resize_to_thumbnail,
        ]

    def get_image(self) -> Image.Image | None:
        return self._crop_frame.src_image

    def change_image(self, new_source: str) -> None:
        self._crop_frame.load_image(new_source)
        self.update_image(self._crop_frame.generate_kivy_image())

    def update_image(self, core_image: CoreImage | None) -> None:
        if core_image is None:
            return

        self.image_texture_property = core_image.texture

    def change_crop_type(self, crop_type: CropType) -> None:
        self._crop_frame.crop_type = crop_type

    def change_width_part(self, new_width: int) -> None:
        self._crop_frame.width_part = new_width
        self.update_image(self._crop_frame.generate_kivy_image())

    def change_height_part(self, new_height: int) -> None:
        self._crop_frame.height_part = new_height
        self.update_image(self._crop_frame.generate_kivy_image())

    def change_background(self) -> None:
        if self.bg_color == [1, 1, 1, 1]:
            self.bg_color = [0, 0, 0, 1]
        else:
            self.bg_color = [1, 1, 1, 1]

    def crop_image(self) -> List[Image.Image]:
        return self._crop_frame.crop_image()

    def move_x(self, delta: int) -> None:
        self._crop_frame.frame_zero_x += delta

        self.update_image(self._crop_frame.generate_kivy_image())

    def move_y(self, delta: int) -> None:
        self._crop_frame.frame_zero_y += delta

        self.update_image(self._crop_frame.generate_kivy_image())

    def resize_width(self, delta: int) -> None:
        self._crop_frame.segment_width += delta

        self.update_image(self._crop_frame.generate_kivy_image())

    def resize_height(self, delta: int) -> None:
        self._crop_frame.segment_height += delta

        self.update_image(self._crop_frame.generate_kivy_image())

    def _start_repeating(self, delta: int, resize_func: ResizeFunction) -> None:
        resize_func(delta)

        clock_event = Clock.schedule_interval(lambda _: resize_func(delta), .15)

        active_func_clock = self._active_clocks.get(resize_func.__name__, [])
        active_func_clock.append(clock_event)

        self._active_clocks[resize_func.__name__] = active_func_clock

    def _stop_repeating(self, resize_func: ResizeFunction) -> None:
        for active_clock in self._active_clocks[resize_func.__name__]:
            Clock.unschedule(active_clock)
