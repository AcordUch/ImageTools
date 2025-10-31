from pathlib import Path
from PIL import Image
from math import floor

from common.src.resizers.cropped import resize_to_thumbnail, resize_to_width, resize_to_height
from common.src.resizers.original import adjust_to_dividers, resize_to_square
from common.src.croppers.domain import CropType
from common.src.croppers.crop import crop_many

from console.src.internal.config import AppConfig


class ImageProcessor:
    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config

    def process(self, img_path: Path, save_path: Path) -> None:
        save_file_name = self.app_config.save_filename if self.app_config.save_filename is not None else img_path.stem

        with Image.open(img_path) as img:
            img.load()

            resized_img = adjust_to_dividers(img, self.app_config.width_part, self.app_config.height_part)

            match self.app_config.crop_type:
                case CropType.SQUARE:
                    src_img = resize_to_square(resized_img, self.app_config.width_part, self.app_config.height_part)
                    image_transforms = [
                        resize_to_thumbnail,
                    ]
                case CropType.WIDTH:
                    src_img = resized_img
                    image_transforms = [
                        resize_to_width,
                        resize_to_thumbnail,
                    ]
                case CropType.HEIGHT:
                    src_img = resized_img
                    image_transforms = [
                        resize_to_height,
                        resize_to_thumbnail,
                    ]

            src_width, src_height = src_img.size
            width_part_size, height_part_size = floor(src_width / self.app_config.width_part), floor(src_height / self.app_config.height_part)

            cropped_img_list = crop_many(src_img, self.app_config.width_part, self.app_config.height_part, width_part_size, height_part_size, image_transforms)
            for i in range(len(cropped_img_list)):
                cropped_img_list[i].save(save_path / Path(f"{save_file_name}_{str(i)}{self.app_config.save_file_type}"))
