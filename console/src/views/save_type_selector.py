from rich.console import Console

from console.src.views.common import CurrentView, View, InputFunction, InputReader
from console.src.internal.config import AppConfig


class SavePartSelector(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

    def draw(self) -> InputReader:
        self.console.clear()

        self.console.print("""Выберете формат для сохранения: 
    1 - .png
    """)
        return InputReader.with_autocomplete()

    def on_input(self, input_read: InputFunction) -> CurrentView:
        inpt = input_read()
        match inpt:
            case ">q" | ">back" | ">exit":
                return CurrentView.MAIN_MENU
            case "1":
                self.app_config.save_file_type = ".png"
                return CurrentView.MAIN_MENU
            case _:
                return CurrentView.SAVE_TYPE_SELECTOR
