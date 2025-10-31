from __future__ import annotations

from enum import Enum
from abc import ABC, abstractmethod
from typing import Callable
from questionary import autocomplete, select, rawselect, Style
from prompt_toolkit.application.current import get_app

from prompt_toolkit import prompt

from rich.console import Console

from console.src.internal.config import AppConfig

type InputFunction = Callable[..., str]


class CurrentView(Enum):
    MAIN_MENU = 0
    CROP_TYPE_SELECTOR = 1
    CROP_PARTS_SELECTOR = 2
    SAVE_TYPE_SELECTOR = 3
    IMAGE_CROP_SCREEN = 4
    CHANGE_SAVE_PATH = 5


class InputReader:
    DEFAULT_HINT_STYLE = Style([
        ('answer', 'fg:#c40a0a bold'),
        ('highlighted', 'bg:#1e4011 bold'),
    ])

    DEFAULT_INSTRUCTION="Используйте цифры или стрелки для выбора"

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
    def preset_input(preset: str) -> InputReader:
        return InputReader(lambda **kwargs: preset)

    def read(self, **kwargs) -> str:
        return self.input_func(**kwargs)


class View(ABC):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        self.app_config: AppConfig = app_config
        self.console: Console = console

    @abstractmethod
    def draw(self) -> InputReader:
        pass

    @abstractmethod
    def on_input(self, input_read: InputReader) -> CurrentView:
        pass
