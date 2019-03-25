"""
*  Author:   Vincent Yim
*  FileName: ip_query.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import requests


class IPQueryAPI:
    """
    这里使用了天气网的ip查询API，没有调用次数、频率和IP限制
    """
    def __init__(self):
        self._base_url = "https://ip.tianqiapi.com/"
        self.requests = requests

    def get_location(self, ip):
        """
        查询IP所在地及运营商信息
        :param ip: IP
        :return: {
                    "ip":"x.x.x.x",
                    "country":"xx",
                    "province":"xxx",
                    "city":"xxx",
                    "isp":"xx"
                }
        """
        res = self.requests.get(url=self._base_url, params={"ip": ip})
        return res.json()


ip_query = IPQueryAPI()

