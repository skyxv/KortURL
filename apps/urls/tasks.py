"""
*  Author:   Vincent Yim
*  FileName: tasks.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
from __future__ import absolute_import, unicode_literals
from KortURL.celery_app import app
from apps.urls.models import LinkMap, AccessLogs


@app.task
def record_log_and_visit_count(ip, code, user_agent):
    """
    日志和访问次数记录
    """
    LinkMap.objects.add_hit_count(code)
    AccessLogs.objects.build_log_from_request(ip, code, user_agent)
