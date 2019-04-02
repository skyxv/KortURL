from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from apps.urls.models import LinkMap, AccessLogs
from .serializers import LinkMapSerializer


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


class HistoryDetail(View):
    """
    历史记录详情
    """
    @method_decorator(login_required)
    def get(self, request, code):
        link_map = get_object_or_404(LinkMap, created_by=request.user, code=code)
        current_url_logs = AccessLogs.objects.get_log_by_code(link_map.code)
        # 访问量
        view_counts, view_dates = self.get_views_count_data(current_url_logs)
        return render(request, 'history_detail.html', locals())

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
