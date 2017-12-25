# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import  HttpResponse,JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

@login_required
def firstpage(request):
    return render(request,'index2.html')


def hello(request):
    lans = [1,2,3,4,5]
    users = [
        {'name':'name1','id':1},
        {'name':'name2','id':2},
        {'name':'name3','id':3},
    ]
    context = {}
    context['users'] = users
    context['username'] = '51reboot'
    context['lans'] = lans
    context['n1'] = random.randint(0,99)
    context['n2'] = random.randint(0,99)
    return render(request,'hello.html',context)

def add(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

def add2(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))

def users(request,**kwargs):
    pk1 = kwargs.get('pk')
    return HttpResponse(pk1)

def argstest(request):
    name = request.GET.get('username')
    uid = request.GET.get('id')
    ret = {'name':name,'id':uid}
    return JsonResponse(ret)


# @csrf_exempt
def add3(request):
    a = request.POST.get('a')
    b = request.POST.get('b')
    c = int(a) + int(b)
    return HttpResponse(str(c))



# @csrf_exempt
def mylogin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        ret = {}
        if user is not None:
            login(request,user)
            ret['status'] = 0
        else:
            ret['status'] = 1
        return JsonResponse(ret)

