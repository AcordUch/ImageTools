"""Операции над изначальным изображением"""

from math import floor
from PIL import Image


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
