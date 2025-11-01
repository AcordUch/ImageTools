from enum import IntEnum, auto
from typing import List
from rich.rule import Rule

type _LoggableObject = str | Rule


class LogLevel(IntEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class LogsHandler:
    def __init__(self):
        self.log_level: LogLevel = LogLevel.INFO

        self._logs: List[_LoggableObject] = []

    @property
    def logs(self) -> List[_LoggableObject]:
        return self._logs

    def debug(self, log: _LoggableObject) -> None:
        self._log(LogLevel.DEBUG, "#adadad", log)

    def info(self, log: _LoggableObject) -> None:
        self._log(LogLevel.INFO, "#575757", log)

    # noinspection PyUnreachableCode
    def _log(self, log_level: LogLevel, log_format: str, log: _LoggableObject) -> None:
        if log_level >= self.log_level:
            match log:
                case str():
                    self._logs.append(f"[{log_format}]{log}[/]")
                case Rule():
                    log.style = log_format
                    self._logs.append(log)
                case _:
                    self._logs.append(f"unexpected log object: {str(log)}")

    def clear_logs(self) -> None:
        self._logs = []
