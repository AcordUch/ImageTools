from questionary import Choice
from rich.console import Console

from common.src.logs import logger, LogLevel

from console.src.views.common import CurrentView, View, InputReader
from console.src.internal.config import AppConfig


class DebugToolsMain(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

    def draw(self) -> InputReader:
        self.console.clear()

        self.console.print(f"Текущий уровень логов: {logger.log_level}")

        self._print_message_from_buffer()
        self._clear_message_buffer()

        return InputReader.with_select()

    def on_input(self, input_reader: InputReader) -> CurrentView:
        inpt = input_reader.read(
            message="",
            choices=[
                Choice("Выйти", ">quit"),
                Choice("Проверить логи", "check_logs"),
                Choice("Сменить уровень логирования", "change_log_level"),
            ],
            use_shortcuts=True,
            style=InputReader.DEFAULT_HINT_STYLE,
            instruction=InputReader.DEFAULT_INSTRUCTION,
        )
        match inpt:
            case ">q" | ">quit" | ">exit":
                return CurrentView.MAIN_MENU
            case "check_logs":
                self._message_buffer += logger.logs
                return CurrentView.DEBUG_TOOLS_MAIN
            case "change_log_level":
                logger.log_level = LogLevel.INFO if logger.log_level == LogLevel.DEBUG else LogLevel.DEBUG
                return CurrentView.DEBUG_TOOLS_MAIN
            case _:
                return CurrentView.DEBUG_TOOLS_MAIN
