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
        self._redis_host = settings.REDIS_STUFF.get('HOST', 'localhost')
        self._redis_port = settings.REDIS_STUFF.get('PORT', 6379)
        self._password = settings.REDIS_STUFF.get('PASSWORD', None)
        self._db = settings.REDIS_STUFF.get('MAP_CACHE_DB', 0)
        self._pool = redis.ConnectionPool(host=self._redis_host, port=self._redis_port,
                                          decode_responses=True, db=self._db,
                                          password=self._password)
        self.client = redis.Redis(connection_pool=self._pool)

    def set_data(self, key, value):
        return self.client.set(key, value)

    def get_data(self, key):
        return self.client.get(key)


redis_cli = RedisClient()
