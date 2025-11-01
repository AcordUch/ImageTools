from pathlib import Path
from typing import List, Mapping

from common.src.domain.domain import CropType
from common.src.resizers.origin_transformer import OriginImageTransformer


class AppConfig:
    _DEFAULT_SAVE_FILE_NAME = "{Исходное имя}"

    def __init__(self):
        self.filename: str | None = None
        self.crop_type: CropType = CropType.SQUARE
        self.width_part: int = 1
        self.height_part: int = 1

        self.save_file_type: str = ".png"
        self.relative_path: Path = Path("./")
        self.save_filename: str | None = None

        self._transformers: Mapping[CropType, List[OriginImageTransformer]] = {
            CropType.SQUARE: [],
            CropType.WIDTH: [],
            CropType.HEIGHT: []
        }

    def transformers(self, crop_type: CropType) -> List[OriginImageTransformer]:
        return self._transformers.get(crop_type, [])

    def set_transformers(self, crop_type: CropType, transformers: List[OriginImageTransformer]) -> None:
        self._transformers[crop_type] = transformers

    def get_save_filename_or_default(self) -> str:
        return self.save_filename if self.save_filename is not None else self._DEFAULT_SAVE_FILE_NAME

    def get_beauty_save_filename(self) -> str:
        return f"{self.get_save_filename_or_default()}_{{Индекс}}{self.save_file_type}"
