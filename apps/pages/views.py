from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from apps.urls.models import LinkMap
from .serializers import LinkMapSerializer


class Doc(TemplateView):
    """
    接口文档
    """
    template_name = 'doc.html'


class LinkMapView(TemplateView):
    """
    接口文档
    """
    template_name = 'history.html'


class History(View):
    """
    历史记录
    """

    @method_decorator(login_required)
    def get(self, request):
        return JsonResponse(LinkMapSerializer(LinkMap.objects.filter(created_by=request.user),
                                              many=True).data, safe=False)


