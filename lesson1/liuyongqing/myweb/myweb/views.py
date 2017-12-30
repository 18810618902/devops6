# -*- coding:utf8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def firstpage(request):
    print request.user
    # return HttpResponse('Hello django! Is Root')
    return render(request,'index2.html')

def mylogin(request):
    print request.user
    if request.method == 'GET':
        return render(request,'pages/examples/login.html')
    if request.method == 'POST':
        name=request.POST.get('username',None)
        passwd=request.POST.get('passwd',None)
        ret={}
        user=authenticate(username=name,password=passwd)
        if user is not None: #用户存在，给他登陆系统的权限。
            login(request,user) #登陆
            ret['status']=0
        else:
            ret['status']=1
        print ret
        return JsonResponse(ret)
