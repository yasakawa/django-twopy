# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
# handler500='ext.exception_logger.server_error'
from django.views.generic import RedirectView
from djtwopy.views import *

urlpatterns = patterns('',
    url(r'^$', top),
    url(r'^thread/(?P<datnum>.*)/$', thread, name='thread'),
    url(r'^tag/(?P<tag>.*)/$', tag, name='tag'),
)
