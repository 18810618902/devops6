# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import  JsonResponse,HttpResponseRedirect
from django.urls import reverse
from models import  *
# Create your views here.

def login_view(request):
    if request.method == "GET":
        return  render(request,"user/login.html")
    else:
        username = request.POST.get("username","")
        passwd  =  request.POST.get("password","")
        user = authenticate(username=username, password=passwd)
        results = {'code': 0, 'msg': u"Successful"}
        if user:
            login(request, user)
            results['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            results = {'code': 1, 'msg': u"用户名或者密码错误!"}
        return JsonResponse(results)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

def  books_view(request):
    data = [i.todict for i in  Book.objects.all()]
    return  JsonResponse({"code":0, "data":data})

