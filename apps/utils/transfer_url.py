"""
*  Author:   Vincent Yim
*  FileName: transfer_url.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.utils.crypto import get_random_string

from apps.utils.get_configs import config


class CodeGenerator:
    """
    生成短码
    """
    def __init__(self):
        self.code_max_length = config.code_length
        self.code_allow_chars = config.code_allowed_chars

    def get_code(self):
        return get_random_string(length=self.code_max_length, allowed_chars=self.code_allow_chars)


code_generator = CodeGenerator()
