from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseRedirect, Http404

from apps.urls.forms import ShortenUrlForm, ReduceForm
from apps.urls.models import LinkMap, AccessLogs
from apps.utils.get_configs import config


class ShortenUrl(View):
    """
    缩短网址
    """

    def get(self, request):
        return render(request, 'shorten_url.html')

    @method_decorator(login_required)
    def post(self, request):
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            link_map = LinkMap.objects.get_or_create_map(request.user,
                                                         form.cleaned_data.get('raw_url'))[0]
            return render(request, 'shorten_url.html',
                          {"short_url": config.get_short_url(link_map.code)})
        else:
            return render(request, 'shorten_url.html', {"error": form.errors})


class RevertUrl(View):
    """
    还原网址
    """

    def get(self, request):
        return render(request, 'reduce_url.html', {'domain': config.domain})

    @method_decorator(login_required)
    def post(self, request):
        form = ReduceForm(request.POST)
        if form.is_valid():
            link_map = LinkMap.objects.get_map_by_code(request.user,
                                                       config.get_code_by_short_url(form.cleaned_data.get("short_url")))
            return render(request, 'reduce_url.html',
                          {"raw_url": link_map.url if link_map else "not_exist", 'domain': config.domain})
        else:
            return render(request, 'reduce_url.html', {"error": form.errors, 'domain': config.domain})


class RedirectView(View):
    """
    将短网址根据映射重定向至源网址
    """

    def get(self, request, code):
        code = code[:config.code_length]
        url = LinkMap.objects.get_url_by_code(code)
        if not url:
            raise Http404
        # TODO 将日志记录和访问次数记录放入队列中异步处理以加快跳转速度
        LinkMap.objects.add_hit_count(code)
        AccessLogs.objects.build_log_from_request(request, code)
        # 302重定向
        return HttpResponseRedirect(url)
