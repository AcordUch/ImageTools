from pathlib import Path

from common.src.croppers.domain import CropType


class AppConfig:
    def __init__(self):
        self.filename: str | None = None
        self.crop_type: CropType = CropType.SQUARE
        self.width_part: int = 1
        self.height_part: int = 1

        self.save_file_type: str = ".png"
        self.relative_path: Path = Path("./")
        self.save_filename: str | None = None
