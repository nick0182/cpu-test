import random

from kivy.clock import Clock
from kivy.uix.videoplayer import VideoPlayer
from kivymd.app import MDApp


class App(MDApp):
    video_player = VideoPlayer(source="resources/countdown_test.mp4", state='play', options={'allow_stretch': True})
    video_file_length_seconds = 81

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_interval(self.position, 1)
        return self.video_player

    def position(self, dt):
        print("Changing position...")
        # self.video_player.seek(round(random.uniform(0, 1), 1))
        # self.video_player.seek(0.012345679)
        self.video_player.seek(random.randrange(0, 80, 1) / self.video_file_length_seconds)


if __name__ == '__main__':
    App().run()
