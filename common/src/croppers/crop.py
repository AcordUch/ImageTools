from PIL import Image
from common.src.resizers.domain import CroppedImageTransformerFunc

def crop(src_img: Image.Image, width_part_size: int, height_part_size: int, current_width_part: int, current_height_part: int) -> Image.Image:
    zero_width = 0 + width_part_size * current_width_part
    zero_height = 0 + height_part_size * current_height_part

    cropped_img = src_img.crop((zero_width, zero_height, zero_width + width_part_size, zero_height + height_part_size))

    return cropped_img


def crop_many(
        src_img: Image.Image,
        width_part: int, height_part: int,
        width_part_size: int, height_part_size: int,
        image_transforms: list[CroppedImageTransformerFunc]
) -> list[Image.Image]:
    cropped_img_list = list()

    for hp in range(height_part):
        for wp in range(width_part):
            cropped = crop(src_img, width_part_size, height_part_size, wp, hp)
            for image_transform in image_transforms:
                cropped = image_transform(cropped)

            cropped_img_list.append(cropped)

    return cropped_img_list
