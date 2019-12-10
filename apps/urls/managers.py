"""
*  Author:   Vincent Yim
*  FileName: managers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.db import models
from django.utils.timezone import now

from apps.utils.redis.client import redis_cli
from apps.utils.ip_query import ip_query


class LinkMapManager(models.Manager):

    def get_or_create_map(self, user, url):
        link_map = self.filter(created_by=user, url=url).first()
        if link_map:
            return link_map
        else:
            return self.create(created_by=user, url=url)

    def get_map_by_code(self, user, code):
        return self.filter(code=code, created_by=user).first()

    def get_url_by_code(self, code):
        cache_url = redis_cli.get_data(code)
        if cache_url != 0:
            return cache_url
        else:
            link_map = self.filter(code=code).first()
            if link_map:
                redis_cli.set_data(link_map.code, link_map.url)
                return link_map.url
            # 将数据库中没有的短码也放在缓存中，用0标识数据库中尚未存在该值
            else:
                redis_cli.set_data(code, 0)

    def add_hit_count(self, code):
        """
        访问数加1,并记录初次访问时间
        """
        instance = self.filter(code=code).first()
        if instance:
            if not instance.hit_count:
                instance.init_access_at = now()

            instance.hit_count += 1
            instance.save()


class AccessLogManager(models.Manager):

    def get_log_by_code(self, code):
        return self.filter(code=code).order_by('created_at')

    def build_log_from_request(self, ip, code, user_agent_dict):
        ip_data = ip_query.get_location(ip) if ip != "127.0.0.1" else {}
        self.create(code=code, ip=ip, country=ip_data.get("country", None),
                    province=ip_data.get("province", None),
                    city=ip_data.get("city", None), isp=ip_data.get("isp", None),
                    **user_agent_dict)

