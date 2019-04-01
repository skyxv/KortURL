from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from apps.urls.models import LinkMap


class Doc(TemplateView):
    """
    接口文档
    """
    template_name = 'doc.html'


class History(View):
    """
    历史记录
    """

    @method_decorator(login_required)
    def get(self, request):
        histories = LinkMap.objects.filter(created_by=request.user).all()

        return render(request, 'history.html')
