"""
*  Author:   Vincent Yim
*  FileName: serializers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from rest_framework import serializers

from apps.urls.models import LinkMap
from apps.utils.get_configs import config


class LinkMapSerializer(serializers.ModelSerializer):
    """
    history table data serializer
    """
    long_url = serializers.SerializerMethodField()
    short_url = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()
    init_time = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = LinkMap
        fields = ('long_url', 'short_url', 'counts', 'init_time', 'created_at')

    def get_long_url(self, obj):
        return obj.url

    def get_short_url(self, obj):
        return config.get_short_url_(obj.code)

    def get_counts(self, obj):
        return obj.hit_count

    def get_init_time(self, obj):
        return obj.init_access_at

    def get_created_at(self, obj):
        return obj.created_at

