"""
*  Author:   Vincent Yim
*  FileName: transfer_url.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from string import digits, ascii_lowercase, ascii_uppercase

_alpha = digits + ascii_lowercase + ascii_uppercase


def _ten2any(n, b=64):
    assert b <= 64 and n > 1

    res = ""
    while n > 0:
        n, index = divmod(n, b)
        res += _alpha[index]

    return res[::-1]


def get_code(n):
    return _ten2any(n, 62)

