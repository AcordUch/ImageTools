from __future__ import annotations

from collections.abc import Callable

from PIL import Image

from common.src.domain.domain import CropType

type CroppedImageTransformerFunc = Callable[[Image.Image], Image.Image]
type OriginImageTransformerFunc = Callable[[OriginImageTransformInput], Image.Image]


class OriginImageTransformInput:
    def __init__(self, src_img: Image.Image, width_part: int, height_part: int, crop_type: CropType, **kwargs):
        self.src_img = src_img
        self.width_part = width_part
        self.height_part = height_part
        self.crop_type = crop_type
        self.kwargs = kwargs
