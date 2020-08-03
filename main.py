from kivymd.app import MDApp
# from kivymd.uix.list import IRightBodyTouch
# from kivymd.uix.label import MDLabel
# from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

# from widgets.options import *


class Display(Screen):
    received = StringProperty()

    def receive_data(self, data):
        Logger.info('ServerUI: Data received by the Screen')
        self.received = data


class OptionPanel(Screen):
    pass


# class AddressLabel(IRightBodyTouch, MDLabel):
#     pass


class ServerUI(MDApp):
    server = None
    ip_address = (None, None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.deferred)

    def deferred(self, *args):
        pass

    def on_stop(self):
        if self.server:
            self.server.shutdown()
            Logger.info('ServerUI: Server has been shut down.')

    def set_server_reference(self, server, ip, port):
        self.server = server
        self.ip_address = (ip, port)

        Logger.info('ServerUI: Server is running.')
        Logger.info('ServerUI: Server port is {1}. Try {0}:{1}'.format(ip, port))

    def server_callback(self, method, data):
        if method.upper() not in ('GET', 'POST'):
            Logger.warning(f'ServerUI: Method received by app server callback is not recognized! [method = {method}]')
            return

        if method.upper() == 'GET':
            Logger.info('ServerUI: GET request received.')

            try:
                print('GET callback (not implemented!): ', data)
            except:  # noqa: E722
                pass

        elif method.upper() == 'POST':
            Logger.info('ServerUI: POST request received.')

            received: str
            if type(data) == str:
                received = data
            elif type(data) == list:
                received = '\n'.join(data)

            self.root.get_screen('scr2').receive_data(received)


if __name__ == '__main__':
    if True:  # Enable to debug the UI
        instance = ServerUI()
        instance.run()
    else:
        Logger.error('ServerUI: Please do not run the server from here.')

        # from server import run
        # run()
