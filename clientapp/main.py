from kivymd.app import MDApp

# from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import Screen

import threading
from scripts.core import post_request


class Display(Screen):
    send_button = ObjectProperty()
    text_field = ObjectProperty()
    indicator = ObjectProperty()

    request_thread: threading.Thread

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.deferred)

    def deferred(self, *args):
        self.element_setup()

    def element_setup(self):
        self.send_button.ids['lbl_txt'].font_style = 'Button'

    def send_button_callback(self):
        self.indicator.active = True
        self.text_field.focus = False

        self.request_thread = threading.Thread(target=self.send_attempt)
        self.request_thread.daemon = True
        self.request_thread.start()

    def send_attempt(self, *args):
        message = self.text_field.text

        try:
            req = post_request(message=message)
            content = req.content.decode('UTF-8')
            Clock.schedule_once(lambda *args: self.set_helper('success', content), 0.25)
        except Exception as e:
            Clock.schedule_once(lambda dt, e=e: self.set_helper('fail', e), 0.25)

    def set_helper(self, type_, message):  # Putang inang helper color yan ekis kapag success e :(
        if type_ not in ('success', 'fail'):
            return

        if type_ == 'success':
            self.text_field.helper_text = message
            self.text_field._current_error_color = get_color_from_hex('#00C851')

        if type_ == 'fail':
            print(message)  # Do something with error?
            self.text_field.helper_text = 'Message was not sent.'
            self.text_field._current_error_color = get_color_from_hex('#ff4444')

        self.indicator.active = False


class Options(Screen):
    pass


class ClientUI(MDApp):
    port = None
    server = None

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_once(self.deferred)

    # def deferred(self, *args):
    #     pass

    def on_stop(self):
        pass


if __name__ == '__main__':
    instance = ClientUI()
    Window.size = (325, 650)
    instance.run()
