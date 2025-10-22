from kivy.app import App
from views.main_widget import MainWidget

from kivy.lang import Builder

Builder.load_file('views/quantity_widget.kv')
Builder.load_file('views/framing_widget.kv')
Builder.load_file('views/crop_widget.kv')
Builder.load_file('views/io_widget.kv')
Builder.load_file('views/main_widget.kv')

class EmojiCropper(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    EmojiCropper().run()
