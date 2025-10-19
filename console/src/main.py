from PIL import Image
from enum import Enum
from collections.abc import Callable
from math import floor
from logging import exception

type ImageTransform = Callable[[Image.Image], Image.Image]


class CropType(Enum):
    SQUARE = 0
    WIDTH = 1
    HEIGHT = 2


class CropConfig:
    def __init__(self,
                 filename: str, save_filename: str,
                 crop_type: CropType,
                 width_part: int, height_part: int
                 ):
        self.filename = filename
        self.crop_type = crop_type
        self.width_part = width_part
        self.height_part = height_part

        self.save_filename = filename.split(".")[0] if save_filename.strip() == "" else save_filename
        self.save_file_type = ".png"


def adjust_to_dividers(src_img: Image.Image, width_part, height_part):
    src_width, src_height = src_img.size

    width_div = src_width % width_part
    height_div = src_height % height_part

    new_width, new_height = src_width, src_height

    if width_div != 0:
        new_width = src_width + width_part - width_div

    if height_div != 0:
        new_height = src_height + height_part - height_div

    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    new_image.paste(src_img, (0, 0))

    return new_image


# Операция над уже вырезанной частью
def resize_to_width(crop_img: Image.Image) -> Image.Image:
    part_width, part_height = crop_img.size

    is_need_reduce = part_height > part_width
    if is_need_reduce:
        new_width, new_height = part_width, part_width
        height_padding = floor((part_height - new_height) / 2)

        return crop_img.crop((0, height_padding, new_width, height_padding + new_height))

    new_width, new_height = part_width, part_width
    height_padding = floor((new_height - part_height) / 2)

    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    new_image.paste(crop_img, (0, height_padding))

    return new_image


# Операция над уже вырезанной частью
def resize_to_height(crop_img: Image.Image) -> Image.Image:
    part_width, part_height = crop_img.size

    is_need_reduce = part_width > part_height
    if is_need_reduce:
        new_width, new_height = part_height, part_height
        width_padding = floor((part_width - new_width) / 2)

        return crop_img.crop((width_padding, 0, width_padding + new_width, new_height))

    new_width, new_height = part_height, part_height
    width_padding = floor((new_width - part_width) / 2)

    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    new_image.paste(crop_img, (width_padding, 0))

    return new_image


# Операция над уже вырезанной частью
def resize_to_thumbnail(src_img: Image.Image) -> Image.Image:
    src_img.thumbnail((100, 100))

    return src_img


# Операция над изначальным изображением
def resize_to_square(src_img: Image.Image, width_part: int, height_part: int) -> Image.Image:
    is_width_resized = False

    src_width, src_height = src_img.size
    part_width = floor(src_width / width_part)
    part_height = floor(src_height / height_part)

    if part_width < part_height:
        part_width = part_height
        is_width_resized = True
    else:
        part_height = part_width

    new_width, new_height = part_width * width_part, part_height * height_part

    if is_width_resized:
        padding = floor((new_width - src_width) / 2)
        padded_coords = (padding, 0)
    else:
        padding = floor((new_height - src_height) / 2)
        padded_coords = (0, padding)

    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    new_image.paste(src_img, padded_coords)

    return new_image


def slice_to_crop_width(src_img: Image.Image, width_part: int, current_part: int) -> Image.Image:
    src_width, src_height = src_img.size
    target_width = src_width / width_part
    target_height = src_height

    zero_width = 0 + target_width * current_part
    zero_height = 0

    cropped_img = src_img.crop((zero_width, zero_height, zero_width + target_width, zero_height + target_height))

    return cropped_img


def crop(src_img: Image.Image, width_part_size: int, height_part_size: int, current_width_part: int, current_height_part: int) -> Image.Image:
    zero_width = 0 + width_part_size * current_width_part
    zero_height = 0 + height_part_size * current_height_part

    cropped_img = src_img.crop((zero_width, zero_height, zero_width + width_part_size, zero_height + height_part_size))

    return cropped_img


def crop_many(
        src_img: Image.Image,
        width_part: int, height_part: int,
        width_part_size: int, height_part_size: int,
        image_transforms: list[ImageTransform]
) -> list[Image.Image]:
    cropped_img_list = list()

    for hp in range(height_part):
        for wp in range(width_part):
            cropped = crop(src_img, width_part_size, height_part_size, wp, hp)
            for image_transform in image_transforms:
                cropped = image_transform(cropped)

            cropped_img_list.append(cropped)

    return cropped_img_list


def init_crop_cfg() -> CropConfig:
    def init_filename(input_message: str) -> str:
        return input(input_message)

    def init_file_type(input_message: str) -> str:
        inpt = input(input_message)
        return ".png" if inpt.strip() == "" else inpt

    # noinspection PyTypeChecker
    def init_crop_type(input_message: str) -> CropType:
        while True:
            crop_type_raw = input(input_message)

            match crop_type_raw:
                case "1":
                    return CropType.SQUARE
                case "2":
                    return CropType.WIDTH
                case "3":
                    return CropType.HEIGHT
                case _:
                    continue

    # noinspection PyTypeChecker
    def init_part(input_message: str) -> int:
        while True:
            try:
                res = int(input(input_message))
                if res <= 0:
                    print("Количество должно быть больше нуля")
                    continue

                return res
            except ValueError:
                print("Введите только число")
                continue

    def default_and_skip(input_message: str, default: int) -> int:
        print(input_message)

        return default

    filename = init_filename("Введите название исходного файл без расширения ('file'): ")
    file_type = init_file_type("Введите расширение файла ('.png'). Оставьте строку пустой для дефолтного типа '.png': ")
    save_filename = init_filename("Введите название для новых файлов без расширения ('file'). Оставьте строку пустой для сохранения изначального названия: ")
    crop_type = init_crop_type(
        """Выберете вид разделения: 
        1 - Масштабирование до квадрата изначального изображения. Предпочтительно для разделения по ширине и высоте одновременно (2x2, 3x2, etc)
        2 - Разделение по ширине с масштабирование до квадрата полученного изображения. Поддерживает только 2x1, 3x1, etc
        3 - Разделение по высоте с масштабирование до квадрата полученного изображения. Поддерживает только 1x2, 1x3, etc
        """
    )

    width_part = 1
    height_part = 1

    match crop_type:
        case CropType.SQUARE:
            width_part = init_part("Введите количество по ширине >0: ")
            height_part = init_part("Введите количество по высоте >0: ")
        case CropType.WIDTH:
            width_part = init_part("Введите количество по ширине >0: ")
            height_part = default_and_skip("Применено значение 1 к высоте", 1)
        case CropType.HEIGHT:
            width_part = default_and_skip("Применено значение 1 к ширине", 1)
            height_part = init_part("Введите количество по высоте >0: ")

    return CropConfig(
        filename=f"{filename}{file_type}",
        save_filename=save_filename,
        crop_type=crop_type,
        width_part=width_part,
        height_part=height_part,
    )


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
                    case _:
                        exception(f"Обнаружен неожиданный тип разрезания: {crop_cfg.crop_type}")
                        return

                src_width, src_height = src_img.size
                width_part_size, height_part_size = floor(src_width / crop_cfg.width_part), floor(src_height / crop_cfg.height_part)

                cropped_img_list = crop_many(src_img, crop_cfg.width_part, crop_cfg.height_part, width_part_size, height_part_size, image_transforms)
                for i in range(len(cropped_img_list)):
                    cropped_img_list[i].save(f"{crop_cfg.save_filename}_{str(i)}{crop_cfg.save_file_type}")

                if not continue_parser():
                    return

        except FileNotFoundError:
            print("Указанный файл не найден. Повторите по новой")
            continue
        except Exception as _:
            exception("Произошла неожиданная ошибка во время выполнения програмыы")
            return


if __name__ == "__main__":
    main()
