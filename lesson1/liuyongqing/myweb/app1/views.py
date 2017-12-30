# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render

# Create your views here.
def hello(request):
    return HttpResponse('Hello django!')

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



def ADD(request,a,b):
    pk=int(a)+int(b)
    return HttpResponse(pk)

def argstest(request):
    name=request.GET.get('name',None)
    uid=request.GET.get('id',None)
    ret={'name':name,'id':uid}
    return  JsonResponse(ret)