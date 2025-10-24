import logging
from os import path
from plyer import filechooser
from PIL import Image
from typing import List

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from app.src.views.cropping_widget import CroppingWidget


class IOWidget(BoxLayout):
    cropping_widget: CroppingWidget | None = ObjectProperty(None)
    _file_name = ""
    _file_extension = ".png"

    def __init__(self, **kwargs):
        super(IOWidget, self).__init__(**kwargs)

    def load_image(self):
        logging.debug("Call load_image")
        image_path = filechooser.open_file(title="Pick a file...", filters=[("Image", "*.png", "*.jpg")])[0]
        if image_path:
            self._file_name = path.splitext(path.basename(image_path))[0]
            self.cropping_widget.change_image(image_path)

    def save_image(self):
        logging.debug("Call save_image")

        copped_image: List[Image] = self.cropping_widget.crop_image()

        filechooser.save_file(
            title="Сохранить файл как...",
            path=f"{self._file_name}{self._file_extension}",
            filters=[("Image", "*.png", "*.jpg"), ('Все файлы', '*.*')],
            on_selection=lambda s: self._handle_save_selection(s, copped_image)
        )

    def _handle_save_selection(self, selection: List[str], images: List[Image.Image]) -> None:
        if selection:
            selected_path = selection[0]
            saving_dir = f"{path.dirname(selected_path)}"
            file_name = path.splitext(path.basename(selected_path))[0]

            logging.info(f"Saving to: {saving_dir}")
            logging.info(f"Saving name: {file_name}{self._file_extension}")

            for index in range(len(images)):
                try:
                    saving_path = f"{saving_dir}\\{file_name}_{index}{self._file_extension}"

                    logging.info(f"Saving: {saving_path}")

                    images[index].save(saving_path)
                except Exception as e:
                    print(f"Не удалось сохранить файл: {e}")

        else:
            logging.info("Save cancelled")
