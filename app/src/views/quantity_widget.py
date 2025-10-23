from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty

from app.src.views.cropping_widget import CroppingWidget


class QuantityWidget(BoxLayout):
    quantity_input = StringProperty("1")
    crop_frame_method = StringProperty("")

    cropping_widget: CroppingWidget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(QuantityWidget, self).__init__(**kwargs)

    def increase(self):
        self.quantity_input = str(int(self.quantity_input) + 1)
        getattr(self.cropping_widget, self.crop_frame_method)(int(self.quantity_input))

    def decrease(self):
        new_value = int(self.quantity_input) - 1
        if new_value > 0:
            self.quantity_input = str(new_value)
            getattr(self.cropping_widget, self.crop_frame_method)(int(self.quantity_input))
