# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import JsonResponse
import random

from django.shortcuts import render

# # Create your views here.
# def hello(request):
#     return HttpResponse('Hello django!')

def users(reuqest,pk,pk2):
    print pk
    # a=int(pk)+int(pk2)
    return HttpResponse(pk)

def user1(reuqest,**kwargs):
    print kwargs
    print reuqest.user
    pk1=kwargs.get('pk')
    # a=int(pk)+int(pk2)
    return HttpResponse(pk1)


def hello(request):
    context={}
    # context['SITE_NAME']=settings.SITE_NAME
    context['n1']=random.randint(0,99)
    context['n2']=random.randint(0,50)
    context['name']='lilei'
    context['lags']=['java','python','javascript','php','go']
    context['data']=[
        {'name':'name1','id':1},
        {'name':'name2','id':2},
        {'name':'name3','id':3}
    ]
    print context
    return render(request,'hello.html',context)

def ADD(request,a,b):
    pk=int(a)+int(b)
    return HttpResponse(pk)

def argstest(request):
    name=request.GET.get('name',None)
    uid=request.GET.get('id',None)
    ret={'name':name,'id':uid}
    return  JsonResponse(ret)

def plus(request,n1,n2):
    ret=int(n1)+int(n2)
    return HttpResponse(str(ret))