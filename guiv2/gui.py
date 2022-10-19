from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from hardware.temperature import Temperature


class GuiLayout(AnchorLayout):
    _temperature = Temperature()
    _last_value = -1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source="resources/background flicker.gif", allow_stretch=True))
        self._number_label = Label(text="50", font_size=96)
        self.add_widget(self._number_label)
        self._number_animation = Animation(font_size=192, duration=0.5)

    def position(self, dt):
        current_temperature = self._temperature.fetch_temperature()
        print(f"Current GPU temperature: {current_temperature}")
        if self.temperature_changed(current_temperature):
            self._number_label.text = str(current_temperature)
            self._number_label.font_size = 96
            self._number_animation.start(self._number_label)

    def temperature_changed(self, current_value):
        if current_value != self._last_value:
            self._last_value = current_value
            return True
        else:
            return False


class Gui(App):
    def build(self):
        layout = GuiLayout()
        Clock.schedule_interval(layout.position, 1)
        return layout


if __name__ == '__main__':
    Gui().run()
