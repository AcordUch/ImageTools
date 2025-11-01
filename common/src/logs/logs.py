from typing import List


class LogsHandler:
    def __init__(self):
        self._logs: List[str] = []

    @property
    def logs(self):
        return self._logs

    def append(self, log):
        self._logs.append(log)

    def clear_logs(self):
        self._logs = []