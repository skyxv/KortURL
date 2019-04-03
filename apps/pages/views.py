from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render

from apps.urls.models import LinkMap, AccessLogs
from .serializers import LinkMapSerializer
from .statistic_views import StatisticView


class Doc(TemplateView):
    """
    接口文档
    """
    template_name = 'doc.html'


class LinkMapView(TemplateView):
    """
    我的记录
    """
    template_name = 'history.html'


class History(View):
    """
    当前用户的记录数据
    """

    @method_decorator(login_required)
    def get(self, request):
        return JsonResponse(LinkMapSerializer(LinkMap.objects.filter(created_by=request.user),
                                              many=True).data, safe=False)


class HistoryDetail(StatisticView):
    """
    历史记录详情
    """
    @method_decorator(login_required)
    def get(self, request, code):
        link_map = get_object_or_404(LinkMap, created_by=request.user, code=code)
        current_url_logs = AccessLogs.objects.get_log_by_code(link_map.code)
        # 访问量
        view_counts, view_dates = self.get_views_count_data(current_url_logs)
        # 24小时访问趋势
        trend_hours, trend_counts = self.get_all_day_visit_trend(current_url_logs)
        # 设备统计
        device_names, device_data = self.get_device_data(current_url_logs)
        # 操作系统统计
        os_names, os_data = self.get_os_data(current_url_logs)
        # 浏览器统计
        browser_names, browser_data = self.get_browser_data(current_url_logs)
        # 运营商
        isp_names, isp_data = self.get_isp_data(current_url_logs)
        # 国内访问分布
        max_value, domestic_data = self.get_domestic_data(current_url_logs)
        return render(request, 'history_detail.html', locals())
