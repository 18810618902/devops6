# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import  HttpResponse
from django.http.response import  JsonResponse
from django.shortcuts import render

import json
import random

# Create your views here.
def hello(request):
    # return HttpResponse('hello app1')
    contex={}
    mylist=['pythion','java','go','node']
    users = [
        {'name':'name1','id':1},
        {'name':'name2','id': 2},
        {'name':'nam3','id':3},
    ]
    contex['mylist']=mylist
    contex['users']=users
    contex['n1']=random.randint(0,99)
    contex['n2']=random.randint(0,99)
    return render(request,'hello.html',contex)
def users(request,pk):
    print pk
    #链接数据库，获取pk的数据，转换下格式data
    return HttpResponse(pk)
def users1(request,**kwargs):
    print request.user
    pk1=kwargs.get('pk')
    #链接数据库，获取pk的数据，转换下格式data
    return HttpResponse(pk1)
def add(request,n1,n2):
    return HttpResponse(int(n1)+int(n2))

def argstest(request):
    name=request.GET.get('name')
    uid=request.GET.get('id')
    ret = {'name':name,'id':uid}
    return JsonResponse(ret)