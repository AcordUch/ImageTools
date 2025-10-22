from collections.abc import Callable

type ProcessingFunction = Callable[[any], bool]
type UpdateMarkerFunction = Callable[[any, bool], None]


def text_update_mutex(func):
    def wrapper(self, value):
        if self._is_updating_text:
            return

        self._is_updating_text = True

        func(self, value)

        self._is_updating_text = False

    return wrapper


def update_mutex(processing: ProcessingFunction, update_marker: UpdateMarkerFunction):
    def decorator(func):
        def wrapper(self, *args):
            if processing(self):
                return

            update_marker(self, True)

            func(self, *args)

            update_marker(self, False)

        return wrapper

    return decorator
