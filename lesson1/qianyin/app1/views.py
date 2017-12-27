# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.conf import settings
import datetime
import json
import random


# Create your views here.


# def hello(request):
#     return HttpResponse('Hello App1!')


def users(request, pk):
    print('hello')
    return HttpResponse(pk)


def users1(request, **kwargs):
    print request.user
    pk1 = kwargs.get('pk')
    pk2 = kwargs.get('pk1')
    return HttpResponse("pk1 is %s,pk2 is %s" % (pk1, pk2))


def add(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(c)


def argstest(request):
    name = request.GET.get('name')
    uid = request.GET.get('id')
    ret = {'name': name, 'id': uid}
    return JsonResponse(ret)


def hello(request):
    context = {}
    context['SITE_NAME'] = settings.SITE_NAME #读取settings配置,settings变量命必须大写
    context['n1'] = random.randint(0, 99)
    context['n2'] = random.randint(0, 99)
    context['name'] = 'lilei'
    context['lags'] = ['java', 'python', 'javascript', 'php', 'go']
    context['data'] = [
        {'name':'name1', 'id': 1},
        {'name':'name2', 'id': 2},
        {'name':'name3', 'id': 3},
    ]

    return render(request, 'hello.html', context)

def something(request, s):
    return HttpResponse(s)