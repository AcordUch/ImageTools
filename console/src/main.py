from typing import Mapping

from rich.console import Console

from console.src.internal.config import AppConfig
from console.src.internal.image_processor import ImageProcessor
from console.src.views.common import CurrentView, View, InputFunction
from console.src.views.main_menu import MainMenu
from console.src.views.crop_type_selector import CropTypeSelector
from console.src.views.crop_part_selector import CropPartSelector
from console.src.views.image_crop_screen import ImageCropScreen
from console.src.views.save_type_selector import SavePartSelector
from console.src.views.change_save_path import ChangeSavePath
from console.src.views.transformers_choicer import TransformerChoicer


class Main:
    def __init__(self) -> None:
        self.cfg: AppConfig = AppConfig()
        self.console: Console = Console()
        self.image_processor: ImageProcessor = ImageProcessor(self.cfg)

        self.views: Mapping[CurrentView, View] = {
            CurrentView.MAIN_MENU: MainMenu(self.cfg, self.console),
            CurrentView.CROP_TYPE_SELECTOR: CropTypeSelector(self.cfg, self.console),
            CurrentView.CROP_PARTS_SELECTOR: CropPartSelector(self.cfg, self.console),
            CurrentView.SAVE_TYPE_SELECTOR: SavePartSelector(self.cfg, self.console),
            CurrentView.IMAGE_CROP_SCREEN: ImageCropScreen(self.cfg, self.console, self.image_processor),
            CurrentView.CHANGE_SAVE_PATH: ChangeSavePath(self.cfg, self.console),
            CurrentView.TRANSFORMERS_CHOICER: TransformerChoicer(self.cfg, self.console),
        }

    def main(self) -> None:
        current_view: CurrentView = CurrentView.MAIN_MENU

        while True:
            view = self.views[current_view]
            preset_input = view.draw()

            current_view = view.on_input(preset_input)


if __name__ == "__main__":
    Main().main()
