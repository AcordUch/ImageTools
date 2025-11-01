from os import chdir
from pathlib import Path
from typing import List
from re import compile
from os import path as os_path

from prompt_toolkit.shortcuts import CompleteStyle
from rich.console import Console
from rich.columns import Columns
from rich.rule import Rule

from common.src.logs import logging

from console.src.views.common import CurrentView, View, InputFunction, InputReader
from console.src.internal.config import AppConfig
from console.src.internal.image_processor import ImageProcessor


class ImageCropScreen(View):
    _chdir_regex_name = ">chdir"
    _chname_regex_name = ">chname"
    _rstname_regex_name = ">rstname"
    _chdir_regex = compile(f"{_chdir_regex_name} (.*)")
    _chname_regex = compile(f"{_chname_regex_name} (.*)")
    _rstname_regex = compile(f"{_rstname_regex_name}(.*)")

    _available_commands = [">quit", _chdir_regex_name, _chname_regex_name, _rstname_regex_name]
    _available_commands_hint = {
        ">quit": "Выйти",
        _chdir_regex_name: "Сменить относительный путь сохранения. При сохранении отсутствующие папки будут созданы",
        _rstname_regex_name: "Сбросить имя сохранения до дефолтного",
        _chname_regex_name: ""
    }

    def __init__(self, app_config: AppConfig, console: Console, image_processor: ImageProcessor) -> None:
        super().__init__(app_config, console)

        self._image_processor = image_processor
        self._save_path: Path = Path.cwd() / app_config.relative_path

        self._input_tips: List[str] = []

    def draw(self) -> InputReader:
        self.console.clear()

        self._available_commands_hint[self._chname_regex_name] = f"Сменить имя сохранения. Файлы будут сохранены в виде {{Имя файла}}_{{Индекс}}{self.app_config.save_file_type}"

        self._save_path: Path = Path.cwd() / self.app_config.relative_path

        paths = self._get_dir_and_file()
        files = [p.name for p in paths]
        file_columns = Columns(files, equal=True, expand=True)

        command_columns = Columns(self._available_commands, equal=True, expand=True)

        save_file_infos = [
            f"Путь сохранения: {os_path.normpath(str(self._save_path))}",
            f"Относительный путь сохранения: {self.app_config.relative_path}",
            f"Файл будет сохранен как: {self.app_config.get_beauty_save_filename()}",
            f"Тип файла сохранения: {self.app_config.save_file_type}"
        ]

        self.console.print("Доступные команды:")
        self.console.print(command_columns)
        self.console.print("")

        for info in save_file_infos:
            self.console.print(info)

        self.console.print(Rule(""))
        self.console.print(f"{Path.cwd()}:")
        self.console.print("")
        self.console.print(file_columns)

        self._print_message_from_buffer()
        self.console.print(Rule(""))

        self._input_tips = self._available_commands + files

        self._clear_message_buffer()

        return InputReader.with_autocomplete()

    def on_input(self, input_reader: InputReader) -> CurrentView:
        inpt = input_reader.read(
            message="",
            choices=self._input_tips,
            ignore_case=True,
            complete_style=CompleteStyle.MULTI_COLUMN,
            style=InputReader.DEFAULT_HINT_STYLE,
            meta_information=self._available_commands_hint.copy()
        )
        match inpt:
            case ">q" | ">quit" | ">back" | ">exit":
                return CurrentView.MAIN_MENU

            case path if (match_obj := self._chdir_regex.match(path)):
                self.app_config.relative_path = Path(match_obj.group(1))
                return CurrentView.IMAGE_CROP_SCREEN

            case path if (match_obj := self._chname_regex.match(path)):
                self.app_config.save_filename = match_obj.group(1)
                return CurrentView.IMAGE_CROP_SCREEN

            case path if (match_obj := self._rstname_regex.match(path)):
                self.app_config.save_filename = None
                return CurrentView.IMAGE_CROP_SCREEN

            case _:
                path = Path(inpt)

                if not path.exists():
                    self._messages_to_print.append("\n[red]Введенный путь не существует[/red]")
                    return CurrentView.IMAGE_CROP_SCREEN

                if path.is_dir():
                    chdir(path)
                    return CurrentView.IMAGE_CROP_SCREEN

                if path.is_file():
                    if path.suffix.lower() != ".png":
                        self._messages_to_print.append("\n[red]Выбранный файл не является .png[/red]")
                        return CurrentView.IMAGE_CROP_SCREEN

                    if not self._save_path.exists():
                        self._save_path.mkdir(parents=True, exist_ok=True)

                    self._image_processor.process(path, self._save_path)
                    self._messages_to_print.append("\n[green]Файл успешно сохранён[/green]")

                    return CurrentView.IMAGE_CROP_SCREEN

                return CurrentView.IMAGE_CROP_SCREEN

    @staticmethod
    def _get_dir_and_file() -> List[Path]:
        return list(Path.cwd().iterdir())
