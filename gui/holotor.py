import threading
import time
from os import getenv

from dotenv import load_dotenv
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivymd.app import MDApp, Builder
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout

from auth.auth import authenticate_user
from gui.colors import colors
from hardware.temperature import Temperature

Builder.load_file('resources/holotor.kv')


class HolotorScreenManager(ScreenManager):
    def login(self):
        print("Login process started")
        threading.Thread(target=authenticate_user, args=[self.login_success], daemon=True).start()

    def login_success(self, dt):
        print("Login success!")
        self.current = "Holotors"

    def play_holotor(self):
        print("Playing holotor")
        self.current = "Video"


class LoginScreen(Screen):
    pass


class VideoScreen(Screen):
    holotor_video = ObjectProperty()
    fullscreen_button = ObjectProperty()
    _last_move_time = None
    _mouse_pos_bind_uid = None
    _button_state_event = None

    def start_video(self):
        self._mouse_pos_bind_uid = Window.fbind('mouse_pos', self._store_last_move_time)
        self._button_state_event = Clock.schedule_interval(self._button_state, 0.5)
        self.holotor_video.start()

    def stop_video(self):
        if self._mouse_pos_bind_uid:
            print("Unbind mouse pos")
            Window.unbind_uid('mouse_pos', self._mouse_pos_bind_uid)
        if self._button_state_event:
            print("Unschedule button state")
            Clock.unschedule(self._button_state_event)

    def _store_last_move_time(self, instance, pos):
        if self.collide_point(*pos):
            curr_time = time.time()
            self._last_move_time = curr_time
            self.fullscreen_button.opacity = 1

    def _button_state(self, dt):
        curr_time = time.time()
        if self._last_move_time and curr_time - self._last_move_time > 2:
            print("2 seconds since last mouse pos change have been passed. Closing the button...")
            self.fullscreen_button.opacity = 0
            self._last_move_time = None


class HolotorsScreen(Screen):
    pass


class DisplayModal(ModalView):
    pass


class DisplayLayout(MDBoxLayout):
    pass


class VideoLayout(MDFloatLayout):
    pass


class FullscreenButton(MDIconButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_fullscreen = False

    def resize_screen(self):
        print(f"Resizing screen. current state fullscreen: {self._is_fullscreen}")
        current_state_fullscreen = self._is_fullscreen
        if current_state_fullscreen:
            Window.fullscreen = 0
            self.icon = "resources/expand.png"
        else:
            Window.fullscreen = 'auto'
            self.icon = "resources/shrink.png"
        self._is_fullscreen = not current_state_fullscreen


class HolotorTile(ButtonBehavior, Image, HoverBehavior):
    pass


class HolotorVideo(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        self._configure_styling()
        Window.size = (800, 600)
        return Holotor._create_screen_manager()

    def _configure_styling(self):
        self.theme_cls.colors = colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

    @staticmethod
    def _create_screen_manager():
        sm = HolotorScreenManager()
        if getenv('ENABLE_LOGIN', 'true') == 'true':
            print("Enabling login")
            sm.add_widget(LoginScreen(name="Login"))
        sm.add_widget(HolotorsScreen(name="Holotors"))
        sm.add_widget(VideoScreen(name="Video"))
        return sm


if __name__ == '__main__':
    load_dotenv('resources/.env')
    Holotor().run()
