from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

import os
import imghdr
from datetime import datetime

import threading


class CustomHandler(BaseHTTPRequestHandler):
    ui = None

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('UTF-8'))

        self._GET_processes()

    def do_POST(self):
        self._set_response()

        self._POST_manipulation()

    def _GET_processes(self):
        CustomHandler.ui.server_callback('GET', 'This is from get!')

    def _POST_manipulation(self):
        content_type, params = parse_header(self.headers['content-type'])
        content_length = self.headers['Content-Length']

        if 'boundary' in params:
            params['boundary'] = bytes(params['boundary'], 'UTF-8')
        params['CONTENT-LENGTH'] = content_length

        if content_type == 'multipart/form-data':
            parsed = parse_multipart(self.rfile, params)

            received_dir = 'data/received'

            name = datetime.now().strftime('%Y%m%d_%H%M%S')
            byte_file = parsed['file'][0]
            type_ = imghdr.what(None, h=byte_file)

            full_name = f'{type_.upper()}_{name}.{type_}'
            full_path = os.path.join(received_dir, f'{full_name}')
            with open(full_path, 'wb') as new_file:
                new_file.write(byte_file)

                CustomHandler.ui.server_callback('POST', (received_dir, full_name))

        elif content_type == 'application/x-www-form-urlencoded':
            # parsed = parse(self.rfile)
            # print(parsed)

            content = self.rfile.read(int(content_length))
            parsed = parse_qs(content)

            """
            Supported POST keys(?):
                • b'message'
            """
            supported = [b'message']

            success = True
            if 'message'.encode('UTF-8') in parsed:
                message = parsed['message'.encode('UTF-8')]
                decoded = [item.decode('UTF-8') for item in message]
                CustomHandler.ui.server_callback('POST', decoded)
            # elif:
            #     pass  # For supporting other "keys" in the future?
            else:
                success = False
                message = 'Received POST data not supported. Valid keys are: {}'.format(
                    ', '.join([item.decode('UTF-8') for item in supported])
                )

                self.wfile.write(message.encode('UTF-8'))
                print(f'{message} \nReceived - {parsed}')

            if success:
                self.wfile.write('POST request received successfully.'.encode('UTF-8'))

    # def _get_server_address(self):
    #     return '{}:{}'.format(self.address_string(), self.server.server_port)


def get_IP():
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_:
        sock_.connect(('httpbin.org', 1))
        # sock_.connect(('192.168.254.105', 8000))

        name = sock_.getsockname()  # (ip_address, port)
        return name[0]


def open_server(ui):
    persist = True
    while persist:
        try:
            IP = get_IP()

            # from random import randint
            # PORT = randint(0, 65535)
            # PORT = 58029
            PORT = 8000

            server_address = (IP, PORT)  # Random port number generated might already be in use lol
            httpd = HTTPServer(server_address, CustomHandler)
            CustomHandler.ui = ui

            # httpd.serve_forever()
            thread = threading.Thread(target=httpd.serve_forever)
            thread.daemon = True
            thread.start()

            persist = False
            return httpd, IP, PORT
        except Exception:
            pass
