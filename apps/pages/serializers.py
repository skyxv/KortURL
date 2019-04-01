"""
*  Author:   Vincent Yim
*  FileName: serializers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django.conf import settings
from rest_framework import serializers

from apps.urls.models import LinkMap


class LinkMapSerializer(serializers.ModelSerializer):
    """
    history table data serializer
    """
    long_url = serializers.SerializerMethodField()
    short_url = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()
    init_time = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    @property
    def server_name(self):
        return settings.KORT_URL.get('SERVER_NAME', 'localhost:8000')

    @property
    def code_length(self):
        return settings.KORT_URL.get('CODE_MAX_LENGTH', 7)

    @property
    def domain(self):
        protocol = settings.KORT_URL.get('PROTOCOL', 'HTTPS')
        server_name = self.server_name
        if protocol.lower() in ["https", "http"]:
            return protocol.lower() + "://" + server_name
        else:
            raise ValueError("Incorrect value of 'KORT_URL.PROTOCOL'.")

    def get_short_url_(self, code):
        if self.server_name.endswith('/'):
            return self.domain + code
        else:
            return self.domain + "/" + code

    class Meta:
        model = LinkMap
        fields = ('long_url', 'short_url', 'counts', 'init_time', 'created_at')

    def get_long_url(self, obj):
        return obj.url

    def get_short_url(self, obj):
        return self.get_short_url_(obj.code)

    def get_counts(self, obj):
        return obj.hit_count

    def get_init_time(self, obj):
        return obj.init_access_at

    def get_created_at(self, obj):
        return obj.created_at

