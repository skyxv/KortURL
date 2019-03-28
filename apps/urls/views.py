from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.urls.forms import ShortenUrlForm
from apps.urls.models import LinkMap


class ShortenUrl(View):
    """
    缩短网址
    """
    @property
    def server_name(self):
        return settings.KORT_URL.get('SERVER_NAME', 'localhost:8000')

    def get_short_url(self, code):
        protocol = settings.KORT_URL.get('PROTOCOL', 'HTTPS')
        server_name = self.server_name
        if protocol.lower() in ["https", "http"]:
            if server_name.endswith('/'):
                return protocol.lower() + "://" + server_name + code
            else:
                return protocol.lower() + "://" + server_name + "/" + code
        else:
            raise ValueError("Incorrect value of 'KORT_URL.PROTOCOL'")

    def get(self, request):
        return render(request, 'shorten_url.html')

    @method_decorator(login_required)
    def post(self, request):
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            link_map = LinkMap.objects.get_or_create_map(request.user,
                                                         form.cleaned_data.get('raw_url'),
                                                         form.cleaned_data.get('expire_time'))[0]
            return render(request, 'shorten_url.html',
                          {"short_url": self.get_short_url(link_map.code)})
        else:
            return render(request, 'shorten_url.html', {"error": form.errors})


# Create your views here.
