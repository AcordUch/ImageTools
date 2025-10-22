from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from re import compile as re_compile


class QuantityWidget(BoxLayout):
    quantity_input = StringProperty("1")
    _is_updating_text = False

    def __init__(self, **kwargs):
        super(QuantityWidget, self).__init__(**kwargs)

        self._regex = re_compile("[1-9]\d*")
        self.a= 0

    def validate_input(self, value):
        if self._is_updating_text:
            return

        self._is_updating_text = True

        if value in ["", "-"] or int(value) == 0:
            value = "1"
            self.ids.quantity_input_box.text = "1"

        self._is_updating_text = False