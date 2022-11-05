from kivy.clock import Clock
from kivy.uix.video import Video
from kivymd.app import MDApp

from hardware.temperature import Temperature


class App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._video = Video(source="resources/countdown_test.mp4", state='play', options={'allow_stretch': True})
        self._video_file_length_seconds = 81
        self._temperature = Temperature()
        self._countdown = 0
        self._current_temperature = -1

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_interval(self.position, 1)
        return self._video

    def position(self, dt):
        if self._countdown == 0:
            self._current_temperature = self._temperature.fetch_temperature()
            self._countdown = 4
        if self._video.loaded:
            print(f"Countdown: {self._countdown}; Current CPU temperature: {self._current_temperature}")
            self._video.seek((100 - self._current_temperature) / self._video_file_length_seconds)
        self._countdown -= 1


if __name__ == '__main__':
    App().run()
