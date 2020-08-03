import requests


def get_request(
    address='http://127.0.0.1:8000',
):
    req = requests.get(address)
    # print(req, req.content, req.headers, sep='\n')
    return req


def post_request(
    address='http://127.0.0.1:8000',
    message=None,
    filepath=None,
):
    if (message, filepath).count(None) in (0, 2):
        return 'Invalid parameters'

    if message is not None:
        post_data = {
            'message': message
        }
        req = requests.post(address, data=post_data)

    if filepath is not None:
        post_files = {
            'file': open(filepath, 'rb')
        }
        req = requests.post(address, files=post_files)

    # print(req, req.content, req.headers, sep='\n')
    return req


if __name__ == '__main__':
    # get_request()
    post_request(message='debugdebugdeubg')
