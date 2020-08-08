from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog

from kivy.logger import Logger
from kivy.lang import Builder

from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen

# from ui.options import *

import os
import threading
from server import open_server

from scripts.for_pyinstaller import resource_path

import importlib


class Display(Screen):
    server_image = StringProperty(resource_path('images/blank.jpg'))
    client_image = StringProperty(resource_path('images/blank.jpg'))
    received = StringProperty()

    face_handler = None
    initial_dialog: MDDialog = None
    local_dialog: MDDialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.deferred)

    def deferred(self, *args):
        self.initial_dialog = MDDialog(
            title='Initializing faces',
            text='If this message has been in display for too long, something unintended has probably happened.',
            auto_dismiss=False,
        )
        self.initial_dialog.open()

        thread = threading.Thread(target=self.initialize_handler)
        thread.daemon = True
        Clock.schedule_once(lambda *args: thread.start(), 0.5)

    def initialize_handler(self, *args):
        faces = importlib.import_module('faces')
        self.face_handler = faces.FaceHandler(display=self, frills=self.change_dialog_text)
        self.initial_dialog.dismiss()
        self.initial_dialog = None

    def change_dialog_text(self, text):
        self.initial_dialog.text = text

    def receive_data(self, data):
        if self.initial_dialog is not None:
            return

        Logger.info('ServerUI: Data received by the Screen')
        if os.path.isfile(data):
            self.client_image = data

            self.ids['results_container'].clear_widgets()

            self.local_dialog = MDDialog(
                title='Looking for a match',
                text='Please wait. . .'
            )
            self.local_dialog.open()

            Clock.schedule_once(lambda *args: self.deferred_find_match(data), 1)
        else:
            self.received = data

        self.manager.transition.direction = 'left'
        self.manager.current = self.name

    def deferred_find_match(self, filename):
        matches = self.face_handler.find_match(filename)
        for match in matches:
            temp_name = match.split('/')[-1]
            item = ResultItem(
                image_path=match,
                label_text=temp_name,
            )
            self.ids['results_container'].add_widget(item)

        self.local_dialog.dismiss()


class ResultItem(MDBoxLayout):
    image_path = StringProperty()
    label_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'image_path' in kwargs:
            self.image_path = kwargs['image_path']
        if 'label_text' in kwargs:
            self.label_text = kwargs['label_text']


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

    ui_instance.create_server_reference()

    ui_instance.run()
