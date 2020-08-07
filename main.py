from kivymd.app import MDApp

from kivy.logger import Logger

from kivy.lang import Builder
from kivy.clock import Clock  # noqa
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen

# from ui.options import *

import os
import threading
from server import open_server

from scripts.pyinstaller_absolute_paths import resource_path


class Display(Screen):
    server_image = StringProperty(resource_path('images/blank.jpg'))
    client_image = StringProperty(resource_path('images/blank.jpg'))
    received = StringProperty()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_once(self.deferred, 3)

    # def deferred(self, *args):
    #     self.client_image = 'received/JPEG_20200805_164713.jpeg'

    def receive_data(self, data):
        Logger.info('ServerUI: Data received by the Screen')
        if os.path.isfile(data):
            self.client_image = data
            # self.client_image = 'received/JPEG_20200805_164713.jpeg'
        else:
            self.received = data

        self.manager.transition.direction = 'left'
        self.manager.current = self.name


class OptionPanel(Screen):
    pass


class ServerUI(MDApp):
    server = None
    ip_address = ListProperty([None, None])

    server_is_live = BooleanProperty(False)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_once(self.deferred)

    # def deferred(self, *args):
    #     pass

    def build(self):
        return Builder.load_file(resource_path('main.kv'))

    def create_server_reference(self):
        server, ip, port = open_server(ui=self)
        self.server = server
        self.ip_address = (ip, port)
        self.server_is_live = True

        Logger.info('ServerUI: Live at {}:{}'.format(ip, port))

    def on_stop(self):
        if self.server:
            self.server.shutdown()

        Logger.info('ServerUI: Server has been shut down')

    def toggle_server(self, status):
        if status is True and self.server is None:
            Logger.info('ServerUI: Server is toggled on')

            self.create_server_reference()
        else:
            Logger.info('ServerUI: Server is toggled off')

            thread = threading.Thread(target=self.server.shutdown)
            thread.start()

            self.server = None
            self.ip_address = [None, None]
            self.server_is_live = False

    def server_callback(self, method, data):
        if method.upper() not in ('GET', 'POST'):
            Logger.warning(f'ServerUI: Method received by app server callback is not recognized! [method = {method}]')
            return

        if method.upper() == 'GET':
            Logger.info('ServerUI: GET request received')

            try:
                print('GET callback (not implemented!): ', data)
            except:  # noqa: E722
                print('Printing of GET data failed!')

        elif method.upper() == 'POST':
            Logger.info('ServerUI: POST request received')

            received: str
            if type(data) == str:
                received = data
            elif type(data) == list:
                received = '\n'.join(data)
            elif type(data) == tuple:
                received = '/'.join(data)  # Filepath; I'd use os.path.join() but Kivy does not recognize Windows' style
            else:
                Logger.error('ServerUI: Received file is not supported, check ASAP')
                return

            self.root.get_screen('scr2').receive_data(received)


if __name__ == '__main__':
    ui_instance = ServerUI()

    # server, ip, port = initialize_server(ui_instance)
    # ui_instance.set_server_reference(server, ip, port)
    ui_instance.create_server_reference()

    ui_instance.run()
