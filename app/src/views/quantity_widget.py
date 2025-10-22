from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from app.src.internal.decorator import update_mutex


class QuantityWidget(BoxLayout):
    quantity_input = StringProperty("1")

    _update_marker = False

    def __init__(self, **kwargs):
        super(QuantityWidget, self).__init__(**kwargs)

    def get_update_marker(self) -> bool:
        return self._update_marker

    def set_update_marker(self, marker: bool) -> None:
        self._update_marker = marker

    # noinspection PyTypeChecker
    @update_mutex(get_update_marker, set_update_marker)
    def validate_input(self, value):
        if value in ["", "-"] or int(value) == 0:
            self.ids.quantity_input_box.text = "1"

    def increase(self):
        self.ids.quantity_input_box.text = str(int(self.ids.quantity_input_box.text) + 1)

    def decrease(self):
        self.ids.quantity_input_box.text = str(int(self.ids.quantity_input_box.text) - 1)

    def processing(self):
        return self._update_marker
