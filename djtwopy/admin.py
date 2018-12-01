# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
import .models

class DtThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'title', 'res', 'date_updated')
    search_fields=['title']

class DtCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread_link', 'number', 'line', 'datetime', 'date_updated')
    search_fields=['line']

    def thread_link(self, obj):
        return '<a href="%s">%s</a>' % (reverse('thread', args=[obj.thread.id]), obj.thread.title[0:80])
    thread_link.allow_tags = True

admin.site.register(models.DtThread, DtThreadAdmin)
admin.site.register(models.DtComment, DtCommentAdmin)
