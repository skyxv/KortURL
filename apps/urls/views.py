from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.urls.forms import ShortenUrlForm, ReduceForm
from apps.urls.models import LinkMap


class BaseUrlView(View):
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

    def get_short_url(self, code):
        if self.server_name.endswith('/'):
            return self.domain + code
        else:
            return self.domain + "/" + code

    def get_code_by_short_url(self, short_url):
        if short_url:
            url_pieces = short_url.split(self.domain)
            return url_pieces[1].replace('/', '') if url_pieces[1].startswith('/') else url_pieces[1]


class ShortenUrl(BaseUrlView):
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
                          {"short_url": self.get_short_url(link_map.code)})
        else:
            return render(request, 'shorten_url.html', {"error": form.errors})


class RevertUrl(BaseUrlView):
    """
    还原网址
    """

    def get(self, request):
        return render(request, 'reduce_url.html', {'domain': self.domain})

    @method_decorator(login_required)
    def post(self, request):
        form = ReduceForm(request.POST)
        if form.is_valid():
            link_map = LinkMap.objects.get_map_by_code(request.user,
                                                       self.get_code_by_short_url(form.cleaned_data.get("short_url")))
            return render(request, 'reduce_url.html',
                          {"raw_url": link_map.url if link_map else "not_exist", 'domain': self.domain})
        else:
            return render(request, 'reduce_url.html', {"error": form.errors, 'domain': self.domain})

