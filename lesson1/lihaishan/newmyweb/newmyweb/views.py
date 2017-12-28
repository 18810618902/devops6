# -*- coding: utf-8 -*-
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout #导入鉴权模块和登陆模块
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def firstpage(request):
    return render(request,'index.html')


def mylogin(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=="POST":
        username=request.POST.get("username")
        passwd=request.POST.get("passwd")
        user = authenticate(username=username, password=passwd)
        ret={}
        if user is not None:  #用户存在，登陆系统
            login(request,user)
            ret["status"]=0
        else:
            ret["status"]=1
        return JsonResponse(ret)


def mylogout(request):
    login(request)
    return HttpResponse(reverse("url__login"))





