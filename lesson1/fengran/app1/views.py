# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
import random

def hello(request):
    #return HttpResponse('app1 hello')
    context = {}
    lans = ['python','java', 'go']
    users = [
        {'name':'name1','id':1},
        {'name':'name2','id':2}
    ]
    context['username'] = '51reboot'
    context['lans'] =lans
    context['users'] = users
    context['n1'] = random.randint(00,99)
    context['n2'] = random.randint(00,99)
    return render(request, 'hello.html',context)
def users(request,nid):
    return HttpResponse(nid)
def user1(request,*kwargs):
    print request.user
    pk1 = kwargs.get('pk')

def add(request, a, b):
    rest = int(a) + int(b)
    return HttpResponse(rest)

from django.http import JsonResponse
def argstest(request):
    name = request.GET.get('username')
    uid = request.GET.get('uid')
    ret = {'name':name, 'uid':uid}
    return JsonResponse(ret)