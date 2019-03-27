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
    对redis client的封装, 以便于在本项目中使用
    """
    def __init__(self):
        self._redis_host = settings.REDIS_STUFF.get('HOST', 'localhost')
        self._redis_port = settings.REDIS_STUFF.get('PORT', 3306)
        self._pool = redis.ConnectionPool(host=self._redis_host, port=self._redis_port,
                                          decode_responses=True)

        self.client = redis.Redis(connection_pool=self._pool)

    def set(self, key, value, expire_time):
        if expire_time:
            self.client.set(key, value)
        else:
            self.client.set(key, value, ex=expire_time)

    def get(self, key):
        return self.client.get(key)

