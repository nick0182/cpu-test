from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivymd.app import MDApp

from hardware.temperature import Temperature


class HolotorScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen(self))
        self.add_widget(VideoScreen())


class LoginScreen(Screen):

    def __init__(self, screen_manager, **kw):
        super().__init__(**kw)
        self.name = "Login"
        self.add_widget(LoginLayout(screen_manager))


class VideoScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "Video"
        self.add_widget(VideoLayout())


class LoginLayout(GridLayout):

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(LoginButton(screen_manager))


class LoginButton(Button):

    def __init__(self, screen_manager):
        super().__init__(text="Login", font_size=64)
        self._sm = screen_manager

    def on_release(self):
        print("Login process started")
        self._sm.current = "Video"


class VideoLayout(Video):

    def __init__(self):
        super().__init__(source="resources/countdown_test.mp4", state='play', options={'allow_stretch': True})
        self._video_file_length_seconds = 81
        self._temperature = Temperature()
        self._countdown = 0
        self._current_temperature = -1

    def start(self):
        Clock.schedule_interval(self._position, 1)

    def _position(self, dt):
        if self._countdown == 0:
            self._current_temperature = self._temperature.fetch_temperature()
            self._countdown = 4
        if self.loaded:
            print(f"Countdown: {self._countdown}; Current CPU temperature: {self._current_temperature}")
            self.seek((100 - self._current_temperature) / self._video_file_length_seconds)
        self._countdown -= 1


class Holotor(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return HolotorScreenManager()


if __name__ == '__main__':
    Holotor().run()
