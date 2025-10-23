from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty

from common.src.croppers.domain import CropType
from common.src.croppers.domain import CropFrame


class CroppingWidget(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    _crop_frame: CropFrame = ObjectProperty(CropFrame())

    def __init__(self, **kwargs):
        super(CroppingWidget, self).__init__(**kwargs)

    def change_image(self, new_source: str) -> None:
        self.ids.image_display.source = new_source
        self._crop_frame.load_image(new_source)

        print(f"in change_image in CroppingWidget: {self._crop_frame.crop_type}")
        print(f"in change_image in CroppingWidget: {self._crop_frame.width_part}")
        print(f"in change_image in CroppingWidget: {self._crop_frame.height_part}")

    def change_crop_type(self, crop_type: CropType) -> None:
        self._crop_frame.crop_type = crop_type

    def change_width_part(self, new_width: int) -> None:
        self._crop_frame.width_part = new_width

    def change_height_part(self, new_height: int) -> None:
        self._crop_frame.height_part = new_height

    def change_background(self):
        if self.bg_color == [1, 1, 1, 1]:
            self.bg_color = [0, 0, 0, 1]
        else:
            self.bg_color = [1, 1, 1, 1]
