from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class CropSettingsWidget(BoxLayout):
    cropping_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CropSettingsWidget, self).__init__(**kwargs)

    def on_cropping_widget(self, _, value):
        print("in on_cropping_widget in CropSettingsWidget")
        print(self.ids)
        print(dir(self.ids.crop_types_widget))
        self.ids.crop_types_widget.cropping_widget = value
        self.ids.width_quantity.cropping_widget = value
        self.ids.height_quantity.cropping_widget = value