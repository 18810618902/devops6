# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
import random


def hello(request):
    name = request.GET.get("username")
    context = {}
    context['name'] = name
    lans = ['xxx', 'dsfas', 'pppp']
    users = [{'name': 'lll', 'id': 1}, {'name': 'kkk', 'id': 2}]
    context['lans'] = lans
    context['users'] = users
    context['n1'] = random.randint(0, 99)
    context['n2'] = random.randint(0, 99)
    return render(request, 'index.html', context)


def users(request, pk):
    print(pk)
    # 链接数据库，获取pk的数据，转换格式data
    return HttpResponse(pk)


def add(request, n1, n2):
    return HttpResponse(int(n1) + int(n2))


def user1(request, **kwargs):
    pk1 = kwargs.get('pk')
    return HttpResponse(int(pk1))


def user2(request, **kwargs):
    pk1 = kwargs.get('pk1')
    pk2 = kwargs.get('pk2')
    return HttpResponse(int(pk1) + int(pk2))


def argstest(request):
    name = request.GET.get("username")
    uid = request.GET.get("id")
    result = {'name': name, 'id': uid}
    return JsonResponse(result)


