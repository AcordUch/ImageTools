from typing import List, Callable
from rich.console import Console

from common.src.domain.domain import CropType

from console.src.views.common import CurrentView, View, InputReader
from console.src.internal.config import AppConfig


class CropPartSelector(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

        self._input_handler: Callable[[int], CurrentView] = self._handle_square_width
        self._is_width_choosing: bool = True
        self._need_clear_screen: bool = True

    def draw(self) -> InputReader:
        def _is_width_choosing() -> str | None:
            _preset_input = None
            match self.app_config.crop_type:
                case CropType.SQUARE:
                    self.console.print("Введите количество по ширине >0: ", end="")
                case CropType.WIDTH:
                    self.console.print("Введите количество по ширине >0: ", end="")
                case CropType.HEIGHT:
                    self.console.print("Применено значение 1 к ширине")
                    _preset_input = "1"

            self._input_handler = self._handle_square_width

            return _preset_input

        def _is_height_choosing() -> str | None:
            _preset_input = None
            match self.app_config.crop_type:
                case CropType.SQUARE:
                    self.console.print("Введите количество по высоте >0: ", end="")
                case CropType.WIDTH:
                    self.console.print("Применено значение 1 к высоте")
                    _preset_input = "1"
                case CropType.HEIGHT:
                    self.console.print("Введите количество по высоте >0: ", end="")

            self._input_handler = self._handle_square_height

            return _preset_input

        if self._need_clear_screen:
            self.console.clear()

        preset_input: str | None
        if self._is_width_choosing:
            preset_input = _is_width_choosing()
        else:
            preset_input = _is_height_choosing()

        self._print_message_from_buffer(end="")

        self._clear_message_buffer()

        return InputReader.preset_or_none_input(preset_input)

    def on_input(self, input_reader: InputReader) -> CurrentView:
        inpt = input_reader.read()
        match inpt:
            case ">q" | ">back" | ">exit":
                return CurrentView.MAIN_MENU
            case _:
                try:
                    new_value = int(inpt)
                    if new_value <= 0:
                        self._messages_to_print.append("Количество должно быть больше или равно единицы: ")
                        return CurrentView.CROP_PARTS_SELECTOR

                    return self._input_handler(new_value)
                except ValueError:
                    self._messages_to_print.append("Введите только число: ")
                    return CurrentView.CROP_PARTS_SELECTOR

    def _handle_square_width(self, inpt: int) -> CurrentView:
        self.app_config.width_part = inpt
        self._is_width_choosing = False
        self._need_clear_screen = False

        return CurrentView.CROP_PARTS_SELECTOR

    def _handle_square_height(self, inpt: int) -> CurrentView:
        self.app_config.height_part = inpt
        self._is_width_choosing = True
        self._need_clear_screen = True

        return CurrentView.MAIN_MENU
