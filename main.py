from kivymd.app import MDApp

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class Display(Screen):
    received = StringProperty()

    def receive_data(self, data):
        Logger.info('CustomLog: Data received by the Screen')
        self.received = data


class OptionPanel(Screen):
    pass


class ServerUI(MDApp):
    port = None
    server = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.deferred)

    def deferred(self, *args):
        pass

    def on_stop(self):
        if self.server:
            self.server.shutdown()
            Logger.info('CustomLog: Server has been shut down.')

    def set_server_reference(self, server, ip, port):
        self.ip_address = (ip, port)
        # self.port = port
        self.server = server

        Logger.info('CustomLog: Server is running.')
        Logger.info('CustomLog: Server port is {1}. Try {0}:{1}'.format(ip, port))

    def server_callback(self, method, data):
        if method.upper() not in ('GET', 'POST'):
            Logger.warning(f'CustomLog: Method received by app server callback is not recognized! [method = {method}]')
            return

        if method.upper() == 'GET':
            Logger.info('CustomLog: GET request received.')

            try:
                print('GET callback (not implemented!): ', data)
            except:  # noqa: E722
                pass

        elif method.upper() == 'POST':
            Logger.info('CustomLog: POST request received.')

            received: str
            if type(data) == str:
                received = data
            elif type(data) == list:
                received = '\n'.join(data)

            self.root.get_screen('scr2').receive_data(received)


if __name__ == '__main__':
    if False:  # Enable to debug the UI
        instance = ServerUI()
        instance.run()
    else:
        Logger.error('CustomLog: Please do not run the server from here.')

        # from server import run
        # run()
