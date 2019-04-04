from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseRedirect, Http404

from apps.urls.forms import ShortenUrlForm, ReduceForm
from apps.urls.models import LinkMap
from apps.utils.get_configs import config
from apps.urls.tasks import record_log_and_visit_count


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
            return render(request, 'shorten_url.html', {"short_url": config.get_short_url_(link_map.code)})
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
    @staticmethod
    def get_ip_address(request):
        """
        获取ip地址
        """
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip:
            ip = request.META.get('REMOTE_ADDR', "")
        client_ip = ip.split(",")[-1].strip() if ip else ""
        return client_ip

    @staticmethod
    def get_user_agent_dict(request):
        user_agent = dict()
        user_agent["browser_name"] = request.user_agent.browser.family
        user_agent["os_name"] = request.user_agent.os.family
        user_agent["device"] = request.user_agent.device.family
        user_agent["is_mobile"] = request.user_agent.is_mobile
        user_agent["is_pc"] = request.user_agent.is_mobile
        user_agent["is_bot"] = request.user_agent.is_mobile
        return user_agent

    def get(self, request, code):
        code = code[:config.code_length]
        url = LinkMap.objects.get_url_by_code(code)
        if not url:
            raise Http404
        record_log_and_visit_count.delay(self.get_ip_address(request), code,
                                         self.get_user_agent_dict(request))
        # 302重定向
        return HttpResponseRedirect(url)
