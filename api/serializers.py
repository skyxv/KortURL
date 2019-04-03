"""
*  Author:   Vincent Yim
*  FileName: serializers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import re
from rest_framework import serializers

from apps.urls.models import LinkMap


class CreateLinkMapSerializer(serializers.Serializer):
    raw_urls = serializers.ListField(required=True, max_length=100,
                                     error_messages={'not_a_list': '类型必须是列表(数组)。',
                                                     'empty': '列表(数组)不能为空。',
                                                     'max_length': '列表(数组)长度不能超过100。'})

    @staticmethod
    def is_valid_url(raw_url):
        integrity_pattern = "^(https|http)://.*"
        pattern = "^(https|http)://(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?(([0-9]{1,3}\.){3}[0-9]{1,3}|([0-9a-z_!~*'()-]+\.)*([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\.[a-z]{2,6})(:[0-9]{1,4})?((/?)|(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        if re.match(integrity_pattern, raw_url) and re.match(pattern, raw_url):
            return raw_url

    def create(self, validated_data):
        raw_urls = validated_data.get("raw_urls")
        maps = []
        invalid_urls = []
        if raw_urls:
            for raw_url in raw_urls:
                if self.is_valid_url(raw_url):
                    link_map, created = LinkMap.objects.get_or_create_map(user=self.context["request"].user, url=raw_url)
                    maps.append(link_map)
                else:
                    invalid_urls.append(raw_url)
        return maps, invalid_urls

