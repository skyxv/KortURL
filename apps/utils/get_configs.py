"""
*  Author:   Vincent Yim
*  FileName: get_configs.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.conf import settings


class Configuration:
    @property
    def server_name(self):
        return settings.KORT_URL.get('SERVER_NAME', 'localhost:8000')

    @property
    def code_length(self):
        return settings.KORT_URL.get('CODE_MAX_LENGTH', 7)

    @property
    def domain(self):
        protocol = settings.KORT_URL.get('PROTOCOL', 'HTTPS')
        server_name = self.server_name
        if protocol.lower() in ["https", "http"]:
            return protocol.lower() + "://" + server_name
        else:
            raise ValueError("Incorrect value of 'KORT_URL.PROTOCOL'.")

    def get_short_url_(self, code):
        if self.server_name.endswith('/'):
            return self.domain + code
        else:
            return self.domain + "/" + code

    def get_code_by_short_url(self, short_url):
        if short_url:
            url_pieces = short_url.split(self.domain)
            return url_pieces[1].replace('/', '') if url_pieces[1].startswith('/') else url_pieces[1]


config = Configuration()

