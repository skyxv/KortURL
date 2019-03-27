"""
*  Author:   Vincent Yim
*  FileName: managers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.db import models


class LinkMapManager(models.Manager):

    def save_map(self, url, code, expire_time=None):
        data = dict()
        data["url"] = url
        data["code"] = code
        if expire_time:
            data["expire_time"] = expire_time
        return self.create(**data)




