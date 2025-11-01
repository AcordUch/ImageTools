"""Операции над изначальным изображением"""
from math import floor

from PIL import Image
from rich.rule import Rule

from common.src.resizers.domain import OriginImageTransformInput
from common.src.domain.domain import CropType


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


def adjust_to_dividers(src_img: Image.Image, width_part: int, height_part: int) -> Image.Image:
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


def resize_to_adjust_part_to_square(_input: OriginImageTransformInput) -> Image.Image:
    src_width, src_height = _input.src_img.size
    part_width = floor(src_width / _input.width_part)
    part_height = floor(src_height / _input.height_part)

    if part_width == part_height or not (_input.crop_type == CropType.WIDTH or _input.crop_type == CropType.HEIGHT):
        return _input.src_img

    is_resize_to_width = _input.crop_type == CropType.WIDTH
    target_part_size = max(part_width, part_height)

    new_image_width = target_part_size * _input.width_part if is_resize_to_width else target_part_size + 2
    new_image_height = target_part_size + 2 if is_resize_to_width else target_part_size * _input.height_part

    new_image_width = new_image_width if new_image_width % 2 == 0 else new_image_width + 1
    new_image_height = new_image_height if new_image_height % 2 == 0 else new_image_height + 1

    image_center_x = floor(new_image_width / 2)
    image_center_y = floor(new_image_height / 2)

    src_width_zero_mod = src_width if src_width % 2 == 0 else src_width + 1
    src_height_zero_mod = src_height if src_height % 2 == 0 else src_height + 1

    padding_x = image_center_x - floor(src_width_zero_mod / 2)
    padding_y = image_center_y - floor(src_height_zero_mod / 2)

    resized_img = Image.new("RGBA", (new_image_width, new_image_height), (0, 0, 0, 0))
    resized_img.paste(_input.src_img, (padding_x, padding_y))

    _input.kwargs["logger"].debug(Rule())
    _input.kwargs["logger"].debug(f"src_size: {src_width}, {src_height}")
    _input.kwargs["logger"].debug(f"part_size: {part_width}, {part_height}")
    _input.kwargs["logger"].debug(f"target_part_size: {target_part_size}")
    _input.kwargs["logger"].debug(f"new_src_size: {new_image_width}, {new_image_height}")
    _input.kwargs["logger"].debug(f"ing_center: {image_center_x}, {image_center_y}")
    _input.kwargs["logger"].debug(f"part_size_zero_mod: {src_width_zero_mod}, {src_height_zero_mod}")
    _input.kwargs["logger"].debug(f"padding: {padding_x}, {padding_y}")
    _input.kwargs["logger"].debug(Rule())

    return resized_img
