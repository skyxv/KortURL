from django.http import HttpResponseForbidden

from apps.utils.get_configs import config
from apps.utils.redis.client import redis_cli


class ThrottleMiddleware:
    """
    预防高频请求中间件
    """

    @staticmethod
    def get_ip_address(request):
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip:
            ip = request.META.get('REMOTE_ADDR', "")
        client_ip = ip.split(",")[-1].strip() if ip else ""
        return client_ip

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_ip_address(request)
        rate = config.rate
        if self.can_access(ip, rate):
            response = self.get_response(request)
        else:
            response = HttpResponseForbidden("亲,访问频率太快了,休息一下吧")

        return response

    @staticmethod
    def parse_rate(rate):
        time_map = {"day": 86400, "hour": 3600, "min": 60, "sec": 1}
        rates = rate.split("/")
        return int(rates[0]), time_map[rates[1]]

    def can_access(self, key, rate):
        """
        检查IP对应的key在redis是否存在，如果不存在，设置key为ip,value为1,过期时间为速率对应的值
        如果存在，value+=1， 然后比较value是否大于指定次数，大于则返回请求超过限制
        """
        data = redis_cli.get_data(key)
        max_visit_count, exp_time = self.parse_rate(rate)
        if data:
            visit_count = redis_cli.client.incr(key)
            if visit_count > max_visit_count:
                return False
        else:
            redis_cli.client.setex(key, exp_time, 1)
        return True
