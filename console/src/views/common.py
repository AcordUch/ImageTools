from __future__ import annotations

from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Callable, List
from questionary import autocomplete, select, checkbox, Style

from rich.console import Console

from console.src.internal.config import AppConfig
from common.src.resizers.origin_transformer import OriginImageTransformer

type InputFunction = Callable[..., str | List[OriginImageTransformer]]


class CurrentView(Enum):
    MAIN_MENU = auto()
    CROP_TYPE_SELECTOR = auto()
    CROP_PARTS_SELECTOR = auto()
    SAVE_TYPE_SELECTOR = auto()
    IMAGE_CROP_SCREEN = auto()
    CHANGE_SAVE_PATH = auto()
    TRANSFORMERS_CHOICER = auto()
    DEBUG_TOOLS_MAIN = auto()


class InputReader:
    DEFAULT_HINT_STYLE = Style([
        ('answer', 'fg:#c40a0a bold'),
        ('highlighted', 'bg:#1e4011 bold'),
    ])

    DEFAULT_INSTRUCTION = "Используйте цифры или стрелки для выбора"

    def __init__(self, input_func: InputFunction) -> None:
        self.input_func: InputFunction = input_func

    @staticmethod
    def free_input() -> InputReader:
        return InputReader(lambda **kwargs: input())

    @staticmethod
    def with_autocomplete() -> InputReader:
        return InputReader(lambda **kwargs: autocomplete(**kwargs).ask())

    @staticmethod
    def with_select() -> InputReader:
        return InputReader(lambda **kwargs: select(**kwargs).ask())

    @staticmethod
    def with_checkbox() -> InputReader:
        return InputReader(lambda **kwargs: checkbox(**kwargs).ask())

    @staticmethod
    def preset_or_none_input(preset: str | None) -> InputReader:
        return InputReader(lambda **kwargs: preset if preset is not None else input())

    def read(self, **kwargs) -> str | List[OriginImageTransformer]:
        return self.input_func(**kwargs)


class View(ABC):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        self.app_config: AppConfig = app_config
        self.console: Console = console

        self._message_buffer: List[str] = []

    @abstractmethod
    def draw(self) -> InputReader:
        pass

    @abstractmethod
    def on_input(self, input_read: InputReader) -> CurrentView:
        pass

    def _print_message_from_buffer(self, end="\n") -> None:
        for message in self._message_buffer:
            self.console.print(message, end=end)

    def _clear_message_buffer(self) -> None:
        self._message_buffer = []