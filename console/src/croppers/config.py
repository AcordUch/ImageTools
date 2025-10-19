from common.src.croppers.domain import CropType


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


def init_crop_cfg() -> CropConfig:
    filename = _init_filename("Введите название исходного файл без расширения ('file'): ")
    file_type = _init_file_type("Введите расширение файла ('.png'). Оставьте строку пустой для дефолтного типа '.png': ")
    save_filename = _init_filename("Введите название для новых файлов без расширения ('file'). Оставьте строку пустой для сохранения изначального названия: ")
    crop_type = _init_crop_type(
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
            width_part = _init_part("Введите количество по ширине >0: ")
            height_part = _init_part("Введите количество по высоте >0: ")
        case CropType.WIDTH:
            width_part = _init_part("Введите количество по ширине >0: ")
            height_part = _default_and_skip("Применено значение 1 к высоте", 1)
        case CropType.HEIGHT:
            width_part = _default_and_skip("Применено значение 1 к ширине", 1)
            height_part = _init_part("Введите количество по высоте >0: ")

    return CropConfig(
        filename=f"{filename}{file_type}",
        save_filename=save_filename,
        crop_type=crop_type,
        width_part=width_part,
        height_part=height_part,
    )


def _init_filename(input_message: str) -> str:
    return input(input_message)


def _init_file_type(input_message: str) -> str:
    inpt = input(input_message)
    return ".png" if inpt.strip() == "" else inpt


# noinspection PyTypeChecker
def _init_crop_type(input_message: str) -> CropType:
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
def _init_part(input_message: str) -> int:
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


def _default_and_skip(input_message: str, default: int) -> int:
    print(input_message)

    return default
