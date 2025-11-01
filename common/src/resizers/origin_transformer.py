from __future__ import annotations

from typing import List, Mapping

from common.src.resizers.domain import OriginImageTransformerFunc
from common.src.resizers.original import resize_to_adjust_part_to_square
from common.src.logs import logging
from common.src.domain.domain import CropType


class OriginImageTransformer:
    def __init__(self, func: OriginImageTransformerFunc, description: str):
        self.func = func
        self.description = description

    def __eq__(self, other) -> bool:
        if not isinstance(other, OriginImageTransformer):
            logging.append("[grey]OriginImageTransformer.__eq__ not needed type[/grey]")
            logging.append(f"[grey]OriginImageTransformer type is {type(OriginImageTransformer)}[/grey]")
            logging.append(f"[grey]other type is {type(other)}[/grey]")
            return False

        logging.append("[grey]OriginImageTransformer.__eq__ needed type[/grey]")
        return other.func is self.func

    @staticmethod
    def get_transformers(crop_type: CropType) -> List[OriginImageTransformer]:
        return _TRANSFORMERS_BY_CROP_TYPE.get(crop_type, [])


_TRANSFORMERS_BY_CROP_TYPE: Mapping[CropType, List[OriginImageTransformer]] = {
    CropType.SQUARE: [
        OriginImageTransformer(lambda i: i.src_img, "Просто возвращает само изображение")
    ],
    CropType.WIDTH: [
        OriginImageTransformer(resize_to_adjust_part_to_square, "До-расширение исходного"),
        OriginImageTransformer(lambda i: i.src_img, "Просто возвращает само изображение")
    ],
    CropType.HEIGHT: [
        OriginImageTransformer(resize_to_adjust_part_to_square, "До-расширение исходного"),
        OriginImageTransformer(lambda i: i.src_img, "Просто возвращает само изображение")
    ]
}
