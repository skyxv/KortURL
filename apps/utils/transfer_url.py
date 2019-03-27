"""
*  Author:   Vincent Yim
*  FileName: transfer_url.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.conf import settings
from django.utils.crypto import get_random_string


class CodeGenerator:
    """
    生成短码
    """
    def __init__(self):
        self.code_max_length = settings.KORT_URL.get("CODE_MAX_LENGTH", 7)
        self.code_allow_chars = settings.KORT_URL.get("CODE_ALLOWED_CHARS",
                                                      'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def get_code(self):
        return get_random_string(length=self.code_max_length, allowed_chars=self.code_allow_chars)


code_generator = CodeGenerator()
