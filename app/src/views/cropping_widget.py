from typing import List
from PIL import Image

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.core.image import Image as CoreImage

from common.src.croppers.domain import CropType
from common.src.croppers.domain import CropFrame


class CroppingWidget(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    _crop_frame: CropFrame = ObjectProperty(CropFrame())
    image_texture_property = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CroppingWidget, self).__init__(**kwargs)

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

    def change_background(self):
        if self.bg_color == [1, 1, 1, 1]:
            self.bg_color = [0, 0, 0, 1]
        else:
            self.bg_color = [1, 1, 1, 1]

    def crop_image(self) -> List[Image.Image]:
        return self._crop_frame.crop_image()
