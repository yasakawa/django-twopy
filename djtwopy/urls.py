# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', top),
    url(r'^thread/(?P<datnum>.*)/$', thread, name='thread'),
    url(r'^tag/(?P<tag>.*)/$', tag, name='tag'),
)
