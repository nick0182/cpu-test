import threading
from os import getenv

from dotenv import load_dotenv
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivymd.app import MDApp, Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

from auth.auth import authenticate_user
from gui.colors import colors
from hardware.temperature import Temperature
from system.monitor import Monitor, list_active_monitors

Builder.load_file('resources/holotor.kv')


class HolotorScreenManager(ScreenManager):
    def login(self):
        print("Login process started")
        threading.Thread(target=authenticate_user, args=[self.login_success], daemon=True).start()

    def login_success(self, dt):
        print("Login success!")
        self.current = "Holotors"

    def play_holotor(self, modal_view, display):
        print(f"Playing holotor on display: {display.name}")
        modal_view.dismiss()
        Window.left = display.screen_coordinates[0]
        Window.fullscreen = 'auto'
        self.current = "Video"


class LoginScreen(Screen):
    pass


class VideoScreen(Screen):
    video_layout = ObjectProperty()

    def start_video(self):
        self.video_layout.start()


class HolotorsScreen(Screen):
    pass


class DisplayModal(ModalView):
    pass


class DisplayLayout(MDBoxLayout):
    pass


class DisplayButton(MDRaisedButton):
    def __init__(self, display: Monitor, number: int, modal_view: ModalView, **kwargs):
        super().__init__(**kwargs)
        self.rounded_button = True
        self.set_radius(25)
        print(f"Creating display button: {display}")
        self._display = display
        self._modal_view = modal_view
        self.text = "Display " + str(number) + f" ({self._display.size[0]}x{self._display.size[1]})"


class HolotorTile(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_touch_down=self.show_display)

    def show_display(self, widget, touch):
        print(f"Touch position: {touch.pos}")
        print(f"Image position: {widget.pos}")
        print(f"{touch}")
        if widget.collide_point(*touch.pos):
            # The touch has occurred inside the widgets area. Do stuff!
            print("Touch down event")
            dialog = DisplayModal()
            dialog_layout = DisplayLayout()
            active_displays = list_active_monitors()
            for index in range(0, len(active_displays)):
                dialog_layout.add_widget(DisplayButton(active_displays[index], index + 1, dialog))
            dialog.add_widget(dialog_layout)
            dialog.pos_hint = {'x': touch.sx, 'top': touch.sy}
            dialog.open()


class VideoLayout(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._video_file_length_seconds = 81
        self._temperature = Temperature()
        self._countdown = 0
        self._current_temperature = -1

    def start(self):
        self.state = 'play'
        print(f"Thumbnail: {self.preview}")
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
