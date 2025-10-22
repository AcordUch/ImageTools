from PIL import Image
from math import floor
from os import getcwd

from common.src.resizers.cropped import resize_to_thumbnail, resize_to_width, resize_to_height
from common.src.resizers.original import adjust_to_dividers, resize_to_square
from common.src.croppers.domain import CropType
from common.src.croppers.crop import crop_many
from console.src.croppers.config import init_crop_cfg


def main():
    def continue_parser() -> bool:
        while True:
            inpt = input("Желаете продолжить? (default N) Y/N: ")
            if inpt.strip() == "" or inpt.strip() == "N":
                return False
            elif inpt.strip() == "Y":
                return True

    while True:
        crop_cfg = init_crop_cfg()

        try:
            with Image.open(crop_cfg.filename) as img:
                img.load()

                resized_img = adjust_to_dividers(img, crop_cfg.width_part, crop_cfg.height_part)

                match crop_cfg.crop_type:
                    case CropType.SQUARE:
                        src_img = resize_to_square(resized_img, crop_cfg.width_part, crop_cfg.height_part)
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
                width_part_size, height_part_size = floor(src_width / crop_cfg.width_part), floor(src_height / crop_cfg.height_part)

                cropped_img_list = crop_many(src_img, crop_cfg.width_part, crop_cfg.height_part, width_part_size, height_part_size, image_transforms)
                for i in range(len(cropped_img_list)):
                    cropped_img_list[i].save(f"{crop_cfg.save_filename}_{str(i)}{crop_cfg.save_file_type}")

                if not continue_parser():
                    return

        except FileNotFoundError:
            print(f"Указанный файл не найден. Текущая рабочая директория: {getcwd()} \nПовторите по новой")
            continue


if __name__ == "__main__":
    main()
