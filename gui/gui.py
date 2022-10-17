from kivy.clock import Clock
from kivy.uix.video import Video
from kivymd.app import MDApp

from hardware.temperature import Temperature


class App(MDApp):
    video = Video(source="resources/countdown_test.mp4", state='play', options={'allow_stretch': True})
    video_file_length_seconds = 81
    temperature = Temperature()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_interval(self.position, 1)
        return self.video

    def position(self, dt):
        current_temperature = self.temperature.fetch_temperature()
        print(f"Current GPU temperature: {current_temperature}")
        if self.video.loaded:
            self.video.seek((100 - current_temperature) / self.video_file_length_seconds)


if __name__ == '__main__':
    App().run()
