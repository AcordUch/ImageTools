from prompt_toolkit.shortcuts import CompleteStyle
from questionary import Choice
from rich.console import Console

from common.src.croppers.domain import CropType

from console.src.views.common import CurrentView, View, InputFunction, InputReader
from console.src.internal.config import AppConfig


class CropTypeSelector(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

    def draw(self) -> InputReader:
        self.console.clear()

        self.console.print("""Выберете вид разделения: 
    1 - Масштабирование до квадрата изначального изображения. Предпочтительно для разделения по ширине и высоте одновременно (2x2, 3x2, etc)
    2 - Разделение по ширине с масштабирование до квадрата полученного изображения. Поддерживает только 2x1, 3x1, etc
    3 - Разделение по высоте с масштабирование до квадрата полученного изображения. Поддерживает только 1x2, 1x3, etc
    """)

        return InputReader.with_select()

    def on_input(self, input_reader: InputReader) -> CurrentView:
        inpt = input_reader.read(
            message="",
            choices=[
                Choice("Выйти", ">quit"),
                Choice("До квадрата", "1"),
                Choice("По ширине", "2"),
                Choice("По высоте", "3"),
            ],
            use_shortcuts=True,
            style=InputReader.DEFAULT_HINT_STYLE,
            instruction=InputReader.DEFAULT_INSTRUCTION,
        )
        match inpt:
            case ">q" | ">quit" | ">exit":
                return CurrentView.MAIN_MENU
            case "1":
                self.app_config.crop_type = CropType.SQUARE
                return CurrentView.MAIN_MENU
            case "2":
                self.app_config.crop_type = CropType.WIDTH
                return CurrentView.MAIN_MENU
            case "3":
                self.app_config.crop_type = CropType.HEIGHT
                return CurrentView.MAIN_MENU
            case _:
                return CurrentView.CROP_TYPE_SELECTOR
