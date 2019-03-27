"""
*  Author:   Vincent Yim
*  FileName: custom_tags.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_site_name(value):
    return settings.KORT_URL.get('SITE_NAME', value)


@register.filter
def get_bg_color(value):
    return settings.KORT_URL.get('BACKGROUND_COLOR', value)
