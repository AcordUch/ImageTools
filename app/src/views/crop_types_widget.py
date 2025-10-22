from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

from common.src.croppers.domain import CropType
from app.src.internal.decorator import update_mutex

_check_box_id = "inner_check"

class CropTypeWidget(BoxLayout):
    label_text = StringProperty("Default Text")
    group = StringProperty(None)
    default_active = BooleanProperty(False)
    crop_type_value = ObjectProperty(None)

    disable_check_callback = ObjectProperty(None)
    notify_new_check_callback = ObjectProperty(None)

    _update_marker = False

    def get_update_marker(self) -> bool:
        return self._update_marker

    def set_update_marker(self, marker: bool) -> None:
        self._update_marker = marker

    def __init__(self, **kwargs) -> None:
        super(CropTypeWidget, self).__init__(**kwargs)

    # noinspection PyTypeChecker
    @update_mutex(get_update_marker, set_update_marker)
    def change_crop_type(self, new_crop_type: CropType, active: bool) -> None:
        if not active:
            self.disable_check_callback(new_crop_type, self)
            return

        self.notify_new_check_callback(new_crop_type)


class CropTypesWidget(BoxLayout):
    _current_crop_type: CropType = CropType.SQUARE

    def __init__(self, **kwargs) -> None:
        super(CropTypesWidget, self).__init__(**kwargs)

    def check_disable(self, crop_type: CropType, check_box_widget) -> None:
        if crop_type == self._current_crop_type:
            check_box_widget.ids[_check_box_id].active = True

        self._current_crop_type = crop_type

    def on_check_disable(self, crop_type: CropType) -> None:
        self._current_crop_type = crop_type
