"""
*  Author:   Vincent Yim
*  FileName: get_configs.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import re
from django.conf import settings


class Configuration:
    @property
    def rate(self):
        pattern = "^[0-9]+\/(day|hour|min|sec)$"
        rate = settings.KORT_URL.get('IP_RATE')
        if re.fullmatch(pattern, rate):
            return rate
        else:
            return '30/min'

    @property
    def site_name(self):
        return settings.KORT_URL.get('SITE_NAME', "KortURL")

    @property
    def bg_color(self):
        return settings.KORT_URL.get('BACKGROUND_COLOR', "#3498DB")

    @property
    def company_name(self):
        return settings.KORT_URL.get('COMPANY_NAME', "KortURL")

    @property
    def server_name(self):
        return settings.KORT_URL.get('SERVER_NAME', 'localhost:8000')

    @property
    def code_length(self):
        return settings.KORT_URL.get('CODE_MAX_LENGTH', 7)

    @property
    def code_allowed_chars(self):
        return settings.KORT_URL.get('CODE_ALLOWED_CHARS',
                                     'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

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

