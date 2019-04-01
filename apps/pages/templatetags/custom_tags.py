"""
*  Author:   Vincent Yim
*  FileName: custom_tags.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from django import template

from apps.utils.get_configs import config

register = template.Library()


@register.filter
def get_site_name(value):
    return config.site_name


@register.filter
def get_bg_color(value):
    return config.bg_color


@register.filter
def get_company_name(value):
    return config.company_name


@register.filter
def get_year(value):
    import datetime
    return datetime.datetime.now().year
