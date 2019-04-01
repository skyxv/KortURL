from django.views.generic import TemplateView
from rest_framework.viewsets import ReadOnlyModelViewSet

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


class History(ReadOnlyModelViewSet):
    """
    历史记录
    """
    serializer_class = LinkMapSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return LinkMap.objects.all()
        else:
            return LinkMap.objects.none()

