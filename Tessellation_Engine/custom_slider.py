"""
Extension of the built in Slider class.
Saves previous values on touch down events
"""
from kivy.uix.slider import Slider

class CustomSlider(Slider):
    def __init__(self, **kwargs):
        super(CustomSlider, self).__init__(**kwargs)
        self.previous_value = 0

    def on_touch_down(self, touch):
        super(CustomSlider, self).on_touch_down(touch)
        self.previous_value = self.value
