from typing import List

from questionary import Choice
from rich.console import Console

from console.src.views.common import CurrentView, View, InputReader
from console.src.internal.config import AppConfig

from common.src.resizers.origin_transformer import OriginImageTransformer


class TransformerChoicer(View):
    def __init__(self, app_config: AppConfig, console: Console) -> None:
        super().__init__(app_config, console)

    def draw(self) -> InputReader:
        self.console.clear()

        self.console.print("Выберете какие дополнительные модификации применить к :\n")

        return InputReader.with_checkbox()

    def on_input(self, input_reader: InputReader) -> CurrentView:
        self.app_config.set_transformers(
            self.app_config.crop_type,
            input_reader.read(
                message="",
                choices=self._prepare_choices(),
                style=InputReader.DEFAULT_HINT_STYLE,
            )
        )

        return CurrentView.MAIN_MENU

    def _prepare_choices(self) -> List[Choice]:
        return [
            Choice(transformer.description, transformer, checked=transformer in self.app_config.transformers(self.app_config.crop_type))
            for transformer
            in OriginImageTransformer.get_transformers(self.app_config.crop_type)
        ]
