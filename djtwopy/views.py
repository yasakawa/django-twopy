# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render
from .models import DtThread, DtComment


def top(request):
    threads = DtThread.objects.all().order_by('-date_created')

    return render(request, 'djtwopy/top.html',
                  {'threads':threads },
                    context_instance=RequestContext(request))


def thread(request, datnum):
    tag = request.GET.get('tag', None)

    thread = DtThread.objects.get(filename__exact = datnum + '.dat')
    if tag:
        comments = DtComment.objects.filter(thread__exact=thread, tags__name__in=[tag]).order_by('number')
    else:
        comments = DtComment.objects.filter(thread__exact=thread).order_by('number')

    return render(request, 'djtwopy/thread.html',
                  {'thread':thread, 'comments':comments },
                    context_instance=RequestContext(request))

def tag(request, tag):
    comments = DtComment.objects.filter(tags__name__in=[tag])

    return render(request, 'djtwopy/thread.html',
                  {'thread':thread, 'comments':comments },
                    context_instance=RequestContext(request))
