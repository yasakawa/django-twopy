# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', top),
    url(r'^thread/(?P<datnum>.*)/$', thread, name='thread'),
    url(r'^tag/(?P<tag>.*)/$', tag, name='tag'),
]
