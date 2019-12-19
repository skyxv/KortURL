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


def _any2ten(code, b=64):
    result = 0
    for i in range(len(code)):
        result *= b
        result += _alpha.index(code[i])
    return result


def get_code(n):
    return _ten2any(n, 62)


def get_id(code):
    return _any2ten(code, 62)

