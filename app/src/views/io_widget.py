from plyer import filechooser
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class IOWidget(BoxLayout):
    cropping_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(IOWidget, self).__init__(**kwargs)

    def load_image(self):
        path = filechooser.open_file(title="Pick a file...", filters=[("Image", "*.png", "*.jpg")])
        if path:
            self.cropping_widget.change_image(path[0])
