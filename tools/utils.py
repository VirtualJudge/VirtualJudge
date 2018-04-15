import requests


class HttpUtil(object):
    def __init__(self):
        self._req = requests.session()

    @property
    def requests(self):
        return self._req
