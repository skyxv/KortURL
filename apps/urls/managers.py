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
from apps.utils.transfer_url import get_id


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
        """
        先查短码对应的值是否为约定0值，如果是，则代表之前访问过的该短码不存在，直接返回空
        值不为0, 如果缓存中有短码对应的长网址，则直接返回，如果缓存中没有，
        则先转换得到id, 再去数据库中查，如果有，设置缓存后返回长网址，
        如果没有，将该短码在缓存中的值设置为0(即标识为数据库中尚未存在状态)
        """
        # 先在缓存中的过滤器中查找，如果code有效，则继续访问，否则直接返回
        if redis_cli.get_bloom(code):
            cache_url = redis_cli.get_data(code)
            if cache_url != 0:
                if cache_url is not None:
                    return cache_url
                else:
                    id_ = get_id(code)
                    link_map = self.filter(pk=id_).first()
                    if link_map:
                        redis_cli.set_data(link_map.code, link_map.url)
                        return link_map.url
                    # 将数据库中没有的短码也放在缓存中，用0标识数据库中尚未存在该值
                    else:
                        redis_cli.set_data(code, 0)
            else:  # 查到值为0则表示数据库中尚未存在, 直接返回空，不查询数据库。这个else其实可以直接不写，这里是为了更清晰
                return None
        else:
            return None

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

