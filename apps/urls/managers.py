"""
*  Author:   Vincent Yim
*  FileName: managers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.db import models
from apps.utils.transfer_url import code_generator


class LinkMapManager(models.Manager):

    def get_or_create_map(self, user, url):
        code = code_generator.get_code()
        while self.filter(code=code).exists():
            code = code_generator.get_code()
        data = dict()
        data["created_by"] = user
        data["url"] = url
        data["code"] = code
        return self.get_or_create(url=url, created_by=user, defaults=data)

    def get_map_by_code(self, user, code):
        return self.filter(code=code, created_by=user).first()


class AccessLogManager(models.Manager):

    def get_log_by_code(self, code):
        return self.filter(code=code).order_by('created_at')

