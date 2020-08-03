from kivymd.app import MDApp

from kivy.logger import Logger
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

            Logger.info('ClientUI: Sending success')
            content = req.content.decode('UTF-8')
            Clock.schedule_once(lambda *args: self.set_helper(is_success=True, message=content), 0.25)
        except Exception as e:
            Logger.error(f'ClientUI: An exception has occurred. {e}')
            Clock.schedule_once(lambda dt, e=e: self.set_helper(), 0.25)

    def set_helper(self, is_success=False, message=None):  # Putang inang helper color yan ekis kapag success e :(
        if is_success:  # Message successfully sent
            self.text_field.helper_text = message
            self.text_field._current_error_color = get_color_from_hex('#00C851')

        else:  # Not sent
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
