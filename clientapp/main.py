from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform as KivyPlatform, get_color_from_hex

from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

import os
import threading
from datetime import datetime
from scripts.core import get_request, post_request

if KivyPlatform == 'android':
    from scripts.camera_jvinicius import CameraAndroid


class Display(Screen):
    parent_carousel = ObjectProperty()
    send_button = ObjectProperty()
    text_field = ObjectProperty()
    indicator = ObjectProperty()

    address = ListProperty()

    request_thread: threading.Thread

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_once(self.deferred)

    # def deferred(self, *args):
    #     self.widget_initializations()

    # def widget_initializations(self):
    #     self.send_button.ids['lbl_txt'].font_style = 'Button'

    def camera_button_callback(self):
        try:
            req = get_request(
                address=f'http://{self.address[0]}:{self.address[1]}',
            )

            self.open_camera()
        except Exception as e:
            Logger.warning(f'ClientUI: Connection to server cannot be achieved [{e}]')

            if KivyPlatform == 'android':
                dialog = MDDialog(
                    title='Server cannot be reached',
                    text=f'This action cannot continue \n\n{e}',
                    # text='Please try again.',
                    size_hint=(1, 1),
                )
                dialog.open()

    def open_camera(self):
        # debug_message = 'This should open the camera. . .'
        debug_image = 'exclusions/sample.jpg'

        if KivyPlatform == 'android':
            current_datetime = datetime.now()
            datetime_string = current_datetime.strftime('%Y%m%d_%H%M%S')
            image_name = f'CLIENT_{datetime_string}_'

            CameraAndroid(image_name).take_picture(
                on_complete=lambda *args: Clock.schedule_once(lambda *args_: self.camera_callback(*args), 1)
            )
        else:
            # Snackbar(text=debug_message).show()
            self.camera_callback(debug_image)

    def camera_callback(self, image_dir):
        file_size = os.stat(image_dir).st_size
        if file_size == 0:
            return

        self.indicator.active = True

        self.request_thread = threading.Thread(target=lambda *args: self.send_attempt(image_dir))
        self.request_thread.daemon = True
        self.request_thread.start()

    def send_attempt(self, dir):
        # message = self.text_field.text

        try:
            req = post_request(
                address=f'http://{self.address[0]}:{self.address[1]}',
                # message=message,
                filepath=dir,
            )

            content = req.content.decode('UTF-8')
            Logger.info(f'ClientUI: Sending success [{content}]')
            # Clock.schedule_once(lambda *args: self.set_helper(is_success=True, message=content), 0.25)
        except Exception as e:
            Logger.error(f'ClientUI: An exception has occurred. {e}')
            # Clock.schedule_once(lambda dt, e=e: self.set_helper(), 0.25)

        self.indicator.active = False

    def set_helper(self, is_success=False, message=None):  # Putang inang helper color yan ekis kapag success e :(
        if is_success:  # Message successfully sent
            self.text_field.helper_text = message
            self.text_field._current_error_color = get_color_from_hex('#00C851')

        else:  # Not sent
            self.text_field.helper_text = 'Message was not sent.'
            self.text_field._current_error_color = get_color_from_hex('#ff4444')

        # self.indicator.active = False


class Options(Screen):
    parent_carousel = ObjectProperty()

    def validate_field(self, field):
        if field.hint_text.lower() == 'ip address':
            portions = field.text.split('.')
            error_conditions = (
                len(portions) != 4,
                # not all([portion.isdigit() for portion in portions]) or
                # not all([int(portion) <= 255 for portion in portions])
                not all(
                    [portion.isdigit() and int(portion) <= 255 for portion in portions]
                )
            )

        elif field.hint_text.lower() == 'port':
            port_is_digit = field.text.isdigit()

            MAX_PORT = 65535
            MIN_PORT = 0
            if port_is_digit:
                if int(field.text) > MAX_PORT:
                    field.text = f'{MAX_PORT}'
                if int(field.text) < MIN_PORT:  # Not working? Negative sign is considered as string
                    field.text = f'{MIN_PORT}'

            error_conditions = (
                not port_is_digit,
                not (MIN_PORT <= int(field.text) <= MAX_PORT) if port_is_digit else False
            )

        else:
            return  # You're not even supposed to be here! lulz

        if any(error_conditions) or field.text == '':
            field.error = True

            if not field.focus:
                field.focus = True
                field.focus = False

            if self.parent_carousel.current_slide != self:
                self.parent_carousel.load_slide(self)
        else:
            field.error = False

        field.on_text(field, field.text)


class ClientUI(MDApp):
    ip_address = ListProperty(['192.168.254.105', '8000'])
    server = None

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_once(self.deferred)

    # def deferred(self, *args):
    #     pass

    # def on_stop(self):
    #     pass


if __name__ == '__main__':
    instance = ClientUI()

    if KivyPlatform != 'android':
        Window.size = (325, 650)
    else:
        from android.permissions import request_permissions, Permission  # noqa
        request_permissions([
            Permission.CAMERA,
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])

    instance.run()
