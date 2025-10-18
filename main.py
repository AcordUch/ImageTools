import math

from PIL import Image
from enum import Enum


class CropType(Enum):
    SQUARE = 0
    WIDTH = 1


class CropConfig:
    def __init__(self, crop_type: CropType, width_part: int, height_part: int):
        self.crop_type = crop_type
        self.width_part = width_part
        self.height_part = height_part


def adjust_to_dividers(src_img: Image, width_part, height_part):
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


# Операция над изначальным изображением
def resize_to_square(src_img: Image.Image, width_part: int, height_part: int) -> (Image.Image, int, int):
    is_width_resized = False

    src_width, src_height = src_img.size
    part_width = math.floor(src_width / width_part)
    part_height = math.floor(src_height / height_part)

    if part_width < part_height:
        part_width = part_height
        is_width_resized = True
    else:
        part_height = part_width

    new_width, new_height = part_width * width_part, part_height * height_part

    if is_width_resized:
        padding = math.floor((new_width - src_width) / 2)
        padded_coords = (padding, 0)
    else:
        padding = math.floor((new_height - src_height) / 2)
        padded_coords = (0, padding)

    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    new_image.paste(src_img, padded_coords)

    return new_image, part_width, part_height


def slice_to_crop_width(src_img: Image.Image, width_part: int, current_part: int) -> Image.Image:
    src_width, src_height = src_img.size
    target_width = src_width / width_part
    target_height = src_height

    zero_width = 0 + target_width*current_part
    zero_height = 0

    cropped_img = src_img.crop((zero_width, zero_height, zero_width+target_width, zero_height+target_height))

    return cropped_img


def crop(src_img: Image.Image, width_part_size: int, height_part_size: int, current_width_part: int, current_height_part: int) -> Image.Image:
    zero_width = 0 + width_part_size * current_width_part
    zero_height = 0 + height_part_size * current_height_part

    cropped_img = src_img.crop((zero_width, zero_height, zero_width+width_part_size, zero_height+height_part_size))

    return cropped_img


def crop_many(src_img: Image.Image, width_part: int, height_part: int, width_part_size: int, height_part_size: int) -> list[Image.Image]:
    cropped_img_list = list()

    for hp in range(height_part):
        for wp in range(width_part):
            cropped = crop(src_img, width_part_size, height_part_size, wp, hp)
            cropped.thumbnail((100, 100))

            cropped_img_list.append(cropped)

    return cropped_img_list


def main():
    filename, file_format = "long2", ".png"
    width_part, height_part = int(input("Введите количество по ширине: ")), int(input("Введите количество по высоте: "))

    with Image.open(filename + file_format) as img:
        img.load()

        resized_img = adjust_to_dividers(img, width_part, height_part)
        square_img, width_part_size, height_part_size = resize_to_square(resized_img, width_part, height_part)
        cropped_img_list = crop_many(square_img, width_part, height_part, width_part_size, height_part_size)

        for i in range(len(cropped_img_list)):
            cropped_img_list[i].save(f"{filename}_{str(i)}{file_format}")


if __name__ == "__main__":
    main()
