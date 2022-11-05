from kivy.clock import Clock
from kivy.uix.video import Video
from kivymd.app import MDApp

from hardware.temperature import Temperature


class App(MDApp):
    _video = Video(source="resources/countdown_test.mp4", state='play', options={'allow_stretch': True})
    _video_file_length_seconds = 81
    _temperature = Temperature()
    _last_value = -1

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_interval(self.position, 1)
        return self._video

    def position(self, dt):
        current_temperature = self._temperature.fetch_temperature()
        print(f"Current CPU temperature: {current_temperature}")
        if self._video.loaded:
            if self.temperature_changed(current_temperature):
                self._video.seek((100 - current_temperature) / self._video_file_length_seconds)
                self._video.state = 'play'
                Clock.schedule_once(self.pause_video, 0.5)

    def pause_video(self, dt):
        self._video.state = 'pause'

    def temperature_changed(self, current_value):
        if current_value != self._last_value:
            self._last_value = current_value
            return True
        else:
            return False


if __name__ == '__main__':
    App().run()
