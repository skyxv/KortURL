from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class Doc(TemplateView):
    """
    接口文档
    """
    template_name = 'doc.html'
