"""
*  Author:   Vincent Yim
*  FileName: client.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import redis

from django.conf import settings


class RedisClient:
    """
    对redis client的简单封装, 以便于在本项目中使用
    """
    def __init__(self):
        self._pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                          decode_responses=True, db=settings.MAP_CACHE_DB,
                                          password=settings.REDIS_PASSWORD)
        self.client = redis.Redis(connection_pool=self._pool)

    def set_data(self, key, value):
        return self.client.set(key, value)

    def get_data(self, key):
        return self.client.get(key)

    def set_expire_data(self, key, value, exp_time):
        return self.client.set(key, value, ex=exp_time)


redis_cli = RedisClient()
