#coding=utf-8
__author__ = 'xiyuanbupt'
from django.conf.urls import url
from django.views.generic import TemplateView

from wechatserver.views import get_message,RootViewBase

urlpatterns = [
    url(r'^$',RootViewBase.as_view(),name='server'),
    url(r'^about/',TemplateView.as_view(template_name='about.html')),
]