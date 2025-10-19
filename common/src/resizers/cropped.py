"""Операция над уже вырезанной частью"""

from math import floor
from PIL import Image


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


def resize_to_thumbnail(src_img: Image.Image) -> Image.Image:
    src_img.thumbnail((100, 100))

    return src_img
