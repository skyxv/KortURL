"""
*  Author:   Vincent Yim
*  FileName: managers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
