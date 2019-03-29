"""
*  Author:   Vincent Yim
*  FileName: forms.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import re

from django import forms
from django.conf import settings


class ShortenUrlForm(forms.Form):
    """
    缩短网址表单
    """
    raw_url = forms.CharField(max_length=255, required=True, error_messages={"required": "网址不能为空"})

    def clean_raw_url(self):
        raw_url = self.cleaned_data.get('raw_url')
        integrity_pattern = "^(https|http)://.*"
        pattern = "^(https|http)://(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?(([0-9]{1,3}\.){3}[0-9]{1,3}|([0-9a-z_!~*'()-]+\.)*([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\.[a-z]{2,6})(:[0-9]{1,4})?((/?)|(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        if not re.match(integrity_pattern, raw_url):
            raise forms.ValidationError("请输入以http://或https://开头的完整网址")
        if not re.match(pattern, raw_url):
            raise forms.ValidationError("请输入正确的网址")
        return raw_url


class ReduceForm(forms.Form):
    """
    还原网址表单
    """
    short_url = forms.CharField(max_length=255, required=True, error_messages={"required": "网址不能为空"})

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

    @property
    def pattern(self):
        return "^" + re.escape(self.domain if self.domain.endswith('/') else self.domain + "/") + "\w{" + re.escape(str(self.code_length)) + "}$"

    def clean_short_url(self):
        short_url = self.cleaned_data.get('short_url')
        if not re.match(self.pattern, short_url):
            raise forms.ValidationError("请输入以{}开头的正确网址".format(self.domain))
        return short_url
