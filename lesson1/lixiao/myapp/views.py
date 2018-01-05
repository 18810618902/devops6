# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
import random
# Create your views here.

def hello(request):
    con = {}
#    con['SITE_NAME'] = settings.SITE_NAME  #读取settings配置（settings的变量名必须大写）
    con['n1'] = random.randint(0,99)
    con['n2'] = random.randint(0,99)
    con['name'] = 'reboot'
    con['lags'] = ['java','php','python']
    con['data'] = [
        {'name':'name1','id':1},
        {'name':'name4','id':2},
        {'name':'name3','id':3},
    ]
    return render(request,'hello.html',con)

def user(request, pk):
    print pk
    return HttpResponse(pk)

def add(request, n1,n2):
    return HttpResponse(int(n1)+int(n2))

def users(request, **test):
    print request.user
    result = test.get('res')
    comm = test.get('ok')
    print result
    print comm
    return HttpResponse("res is %s,comm is %s" %(result,comm))

def artest(request):
    name = request.GET.get('name')
    uid = request.GET.get('id')
    result = {'username':name,'id':uid}
    return JsonResponse(result)