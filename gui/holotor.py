import threading

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout

from dotenv import load_dotenv
from gui.colors import colors

from auth.auth import authenticate_user
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
        self._video_layout = VideoLayout()
        self.add_widget(self._video_layout)

    def on_pre_enter(self, *args):
        print("Switching to video")
        self._video_layout.start()


class LoginLayout(MDFloatLayout):

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginButton(screen_manager))


class LoginButton(MDRectangleFlatButton):

    # see https://kivymd.readthedocs.io/en/1.1.1/themes/theming/#kivymd.theming.ThemeManager.accent_color
    def __init__(self, screen_manager):
        super().__init__(text="Login", font_size=32, font_name='resources/Jua-Regular.ttf', size_hint=(.3, .3), pos_hint={'x': .35, 'y': .35})
        self.line_color = "A87575"
        self._sm = screen_manager
        self.bind(on_press=self.login)

    def login(self, dt):
        print("Login process started")
        threading.Thread(target=authenticate_user, args=[self.login_success], daemon=True).start()

    def login_success(self, dt):
        print("Login success!")
        self._sm.current = "Video"


class VideoLayout(Video):

    def __init__(self):
        super().__init__(source="resources/countdown_test.mp4", options={'allow_stretch': True})
        self._video_file_length_seconds = 81
        self._temperature = Temperature()
        self._countdown = 0
        self._current_temperature = -1

    def start(self):
        self.state = 'play'
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
        self.theme_cls.colors = colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Window.size = (800, 600)
        return HolotorScreenManager()


if __name__ == '__main__':
    load_dotenv('resources/.env')
    Holotor().run()
