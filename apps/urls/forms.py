"""
*  Author:   Vincent Yim
*  FileName: forms.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import re

from django import forms


class ShortenUrlForm(forms.Form):
    """
    缩短网址表单
    """
    raw_url = forms.CharField(max_length=255, required=True, error_messages={"required": "网址不能为空"})
    expire_time = forms.IntegerField(required=False)

    def clean_raw_url(self):
        raw_url = self.cleaned_data.get('raw_url')
        integrity_pattern = "^(https|http)://.*"
        pattern = "^(https|http)://(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?(([0-9]{1,3}\.){3}[0-9]{1,3}|([0-9a-z_!~*'()-]+\.)*([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\.[a-z]{2,6})(:[0-9]{1,4})?((/?)|(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        if not re.match(integrity_pattern, raw_url):
            raise forms.ValidationError("请输入以http://或https://开头的完整网址")
        if not re.match(pattern, raw_url):
            raise forms.ValidationError("请输入正确的网址")
        return raw_url
