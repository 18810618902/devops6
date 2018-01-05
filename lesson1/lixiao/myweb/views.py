#coding=utf8
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required
def firstpage(request):
    return render(request,'index2.html')

def mylogin(request):
    if request.method == 'GET':
        return render(request,'pages/examples/login.html')
    if request.method == 'POST':
        username = request.POST.get('username',"")
        passwd = request.POST.get('passwd',"")
        user = authenticate(username=username,password=passwd)
        ret = {"code":0,"errmsg":""}
        if user is not None:
            login(request,user)
            ret['code'] = 0
        else:
            ret['code'] = 1
            ret['errmsg'] = 'username or passwd is error'
        return JsonResponse(ret)
