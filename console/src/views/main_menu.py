from pyexpat.errors import messages
from questionary import Choice
from rich.console import Console

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle

from console.src.views.common import CurrentView, View, InputReader
from console.src.internal.config import AppConfig


class MainMenu(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

    def draw(self) -> InputReader:
        self.console.clear()

        self.console.print(f"""Разделитель изображений.
    Текущий тип сохранения: {self.app_config.save_file_type}  
    Текущий тип разделения: {self.app_config.crop_type}
    Число частей по горизонтали: {self.app_config.width_part}
    Число частей по вертикали: {self.app_config.height_part}
    Относительный путь сохранения: {self.app_config.relative_path}
    
    1 - Перейти к выбору изображения
    2 - Сменить тип разделения
    3 - Сменить число частей
    4 - Относительный путь сохранения
    5 - Сменить тип сохранения
            """)

        return InputReader.with_select()

    def on_input(self, input_reader: InputReader) -> CurrentView:
        inpt = input_reader.read(
            message="",
            choices=[
                Choice("Выйти", ">quit"),
                Choice("Перейти к выбору изображения", "1"),
                Choice("Сменить тип разделения", "2"),
                Choice("Сменить число частей", "3"),
                Choice("Относительный путь сохранения", "4"),
                Choice("Сменить тип сохранения", "5"),
            ],
            use_shortcuts=True,
            style=InputReader.DEFAULT_HINT_STYLE,
            instruction=InputReader.DEFAULT_INSTRUCTION,
        )
        match inpt:
            case ">q" | ">quit" | ">exit":
                exit(1)
            case "1":
                return CurrentView.IMAGE_CROP_SCREEN
            case "2":
                return CurrentView.CROP_TYPE_SELECTOR
            case "3":
                return CurrentView.CROP_PARTS_SELECTOR
            case "4":
                return CurrentView.CHANGE_SAVE_PATH
            case "5":
                return CurrentView.SAVE_TYPE_SELECTOR
            case _:
                return CurrentView.MAIN_MENU
