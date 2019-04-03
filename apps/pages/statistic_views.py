"""
*  Author:   Vincent Yim
*  FileName: statistic_views.py
*  Software: PyCharm
*  Blog:     https://yandenghong.github.io
"""
import heapq

from django.utils import timezone
from django.views import View


class StatisticView(View):
    """
    图表统计类视图
    """
    def get_views_count_data(self, current_url_logs):
        """
        访问量图表数据
        """
        date_times = current_url_logs.values_list('created_at', flat=True).distinct()
        dates = []
        view_counts = []
        for date_time in date_times:
            str_time = self.get_str_time(date_time)
            if str_time not in dates:
                view_counts.append(current_url_logs.filter(created_at=date_time).count())
                dates.append(str_time)
            else:
                view_counts[dates.index(str_time)] += 1
        return view_counts, dates

    @staticmethod
    def get_str_time(raw_time):
        raw_time = timezone.localtime(raw_time)
        return "{}-{}-{}".format(raw_time.year, raw_time.month, raw_time.day)

    @staticmethod
    def get_all_day_visit_trend(current_url_logs):
        """
        24小时访问趋势
        """
        import datetime
        now = datetime.datetime.now()
        hours = []
        view_counts = []
        current_url_logs = current_url_logs.filter(created_at__year=now.year,
                                                   created_at__month=now.month,
                                                   created_at__day=now.day)
        for hour in [x for x in range(24)]:
            hours.append(hour)
            view_counts.append(current_url_logs.filter(created_at__hour=hour).count())
        return hours, view_counts

    @staticmethod
    def get_device_data(current_url_logs):
        """
        设备统计
        """
        device_names = current_url_logs.values_list('device', flat=True)
        data = []
        names = list(set(list(device_names)))
        for device_name in names:
            device_count = current_url_logs.filter(device=device_name).count()
            data.append({"name": device_name, "value": device_count})
        return names, data

    @staticmethod
    def get_os_data(current_url_logs):
        """
        操作系统统计
        """
        os_names = current_url_logs.values_list('os_name', flat=True)
        data = []
        names = list(set(list(os_names)))
        for os_name in names:
            os_count = current_url_logs.filter(os_name=os_name).count()
            data.append({"name": os_name, "value": os_count})
        return names, data

    @staticmethod
    def get_browser_data(current_url_logs):
        """
        浏览器统计
        """
        browser_names = current_url_logs.values_list('browser_name', flat=True)
        data = []
        names = list(set(list(browser_names)))
        for browser_name in names:
            browser_count = current_url_logs.filter(browser_name=browser_name).count()
            data.append({"name": browser_name, "value": browser_count})
        return names, data

    @staticmethod
    def get_isp_data(current_url_logs):
        """
        运营商统计
        """
        isp_names = current_url_logs.values_list('isp', flat=True)
        if all(isp_names):
            data = []
            names = list(set(list(isp_names)))
            for isp_name in names:
                browser_count = current_url_logs.filter(isp=isp_name).count()
                data.append({"name": isp_name, "value": browser_count})
            return names, data
        else:
            return [], []

    @staticmethod
    def get_domestic_data(current_url_logs):
        """
        国内访问分布
        """
        provinces = ["北京", "天津", "上海", "重庆", "河北", "河南", "云南", "辽宁", "黑龙江",
                     "湖南", "安徽", "山东", "新疆", "江苏", "浙江", "江西", "湖北", "广西",
                     "甘肃", "山西", "内蒙古", "陕西", "吉林", "福建", "贵州", "广东", "青海",
                     "西藏", "四川", "宁夏", "海南", "台湾", "香港", "澳门"]
        data = []
        view_counts = []
        for province in provinces:
            view_count = current_url_logs.filter(country="中国", province__contains=province).count()
            data.append({"name": province, "value": view_count})
            view_counts.append(view_count)
        return heapq.nlargest(1, view_counts)[0], data
