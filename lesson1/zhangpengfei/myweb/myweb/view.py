#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def mylogin(request):
    print(request.method)
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        # print(request.POST)
        u = request.POST.get('u')
        p = request.POST.get('p')
        print(u,p)
        user = authenticate(username=u,password=p)
        print(user)
        if user:
            login(request,user)
            return    redirect('/index/')

    return redirect('/login/')

def mylogout(request):
    print(request.user)
    logout(request)
    return HttpResponse('logout success')

@login_required
def index(request):
    print(request.user)
    return render(request,'index.html')