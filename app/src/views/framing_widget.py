from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

from common.src.croppers.domain import CropFrame

class FramingWidget(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(FramingWidget, self).__init__(**kwargs)
        self.crop_frame = CropFrame()

    def change_image(self, new_source):
        self.ids.image_display.source = new_source
        self.crop_frame.pre_init(new_source)

    def change_background(self):
        if self.bg_color == [1, 1, 1, 1]:
            self.bg_color = [0, 0, 0, 1]
        else:
            self.bg_color = [1, 1, 1, 1]