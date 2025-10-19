from collections.abc import Callable
from PIL import Image

type ImageTransform = Callable[[Image.Image], Image.Image]
