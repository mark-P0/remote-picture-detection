from kivymd.app import MDApp

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen

import threading
from server import run as run_server
# from widgets.options import *


class Display(Screen):
    received = StringProperty()

    def receive_data(self, data):
        Logger.info('ServerUI: Data received by the Screen')
        self.received = data


class OptionPanel(Screen):
    pass


class ServerUI(MDApp):
    server = None
    ip_address = ListProperty([None, None])

    server_is_live = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.deferred)

    def deferred(self, *args):
        pass

    def on_stop(self):
        if self.server:
            self.server.shutdown()
            Logger.info('ServerUI: Server has been shut down')

    def toggle_server(self, status):
        if status is True and self.server is None:
            Logger.info('ServerUI: Server is toggled on')

            run_server()
        else:
            Logger.info('ServerUI: Server is toggled off')

            thread = threading.Thread(target=self.server.shutdown)
            thread.start()

            self.server = None
            self.ip_address = [None, None]

    def set_server_reference(self, server, ip, port):
        self.server = server
        self.ip_address = (ip, port)
        self.server_is_live = True

        Logger.info('ServerUI: Server is live at {}:{}'.format(ip, port))

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

            self.root.get_screen('scr2').receive_data(received)


if __name__ == '__main__':
    if False:  # Enable to debug the UI only
        Logger.error('ServerUI: Server itself will not start, only the interface!')
        instance = ServerUI()
        instance.run()
    else:
        Logger.error('ServerUI: Server is not meant to be started from here')
        run_server()
