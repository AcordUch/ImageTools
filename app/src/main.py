import logging
from pathlib import Path

from kivy.app import App
from app.src.views.main_widget import MainWidget

from kivy.lang import Builder


class EmojiCropper(App):
    def build(self):
        Builder.load_file(self._resole_path('views/quantity_widget.kv'))
        Builder.load_file(self._resole_path('views/cropping_widget.kv'))
        Builder.load_file(self._resole_path('views/crop_types_widget.kv'))
        Builder.load_file(self._resole_path('views/crop_settings_widget.kv'))
        Builder.load_file(self._resole_path('views/io_widget.kv'))
        Builder.load_file(self._resole_path('views/main_widget.kv'))

        return MainWidget()

    def _resole_path(self, path: str) -> str:
        return str((Path(self.directory) / Path(path)).resolve())


class Main:
    @staticmethod
    def main():
        EmojiCropper().run()


if __name__ == "__main__":
    Main().main()
