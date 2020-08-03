from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

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

        now = datetime.now()
        filename = now.strftime('%Y%m%d_%H%M%S')

        if content_type == 'multipart/form-data':
            parsed = parse_multipart(self.rfile, params)

            byte_file = parsed['file'][0]
            type_ = imghdr.what(None, h=byte_file)
            with open(f'received/{type_.upper()}_{filename}.{type_}', 'wb') as new_file:
                new_file.write(byte_file)
                print(f'File {filename}.{type_} written.')

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

    def _get_server_address(self):
        return '{}:{}'.format(self.address_string(), self.server.server_port)

    @staticmethod
    def _initialize_ui(ui_class, server, ip, port):
        CustomHandler.ui = ui_class()
        CustomHandler.ui.set_server_reference(server, ip, port)
        CustomHandler.ui.run()


def get_IP():
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_:
        sock_.connect(('httpbin.org', 1))
        # sock_.connect(('192.168.254.105', 8000))

        name = sock_.getsockname()  # (ip_address, port)
        return name[0]


def initialize_server():
    IP = get_IP()

    from random import randint
    PORT = randint(0, 65535)
    # PORT = 58029
    # PORT = 8000

    server_address = (IP, PORT)
    httpd = HTTPServer(server_address, CustomHandler)

    # httpd.serve_forever()
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    return httpd, IP, PORT


def run():
    http_server, ip, port = initialize_server()

    if CustomHandler.ui is None:
        from main import ServerUI
        CustomHandler._initialize_ui(
            ui_class=ServerUI,
            server=http_server,
            ip=ip,
            port=port,
        )
    else:
        CustomHandler.ui.set_server_reference(http_server, ip, port)


if __name__ == '__main__':
    run()
