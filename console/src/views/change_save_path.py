from pathlib import Path
from rich.console import Console

from console.src.views.common import CurrentView, View, InputFunction, InputReader
from console.src.internal.config import AppConfig


class ChangeSavePath(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

    def draw(self) -> InputReader:
        self.console.clear()

        self.console.print("Введите путь относительно текущей локации, где будут сохранены файлы:\n")

        return InputReader.free_input()

    def on_input(self, input_reader: InputReader) -> CurrentView:
        inpt = input_reader.read()
        match inpt:
            case ">q" | ">back" | ">exit":
                return CurrentView.MAIN_MENU
            case _:
                self.app_config.relative_path = Path(inpt)

                return CurrentView.MAIN_MENU
