"""
*  Author:   Vincent Yim
*  FileName: serializers.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from rest_framework import serializers

from apps.urls.models import LinkMap


class LinkMapSerializer(serializers.ModelSerializer):
    """
    history table data serializer
    """
    class Meta:
        model = LinkMap
        fields = ('url', 'code', 'hit_count', 'init_access_at', 'created_at')

