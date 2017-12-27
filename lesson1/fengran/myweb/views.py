#coding=utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required   #登录保护

@login_required()
def index(request):
    return render(request, 'index2.html')

def mylogin(request):   #函数名不能用login
    if request.method == 'GET':
        return render(request, "pages/examples/login.html")
    if request.method == 'POST':
        username = request.POST.get('username')
        print username
        password = request.POST.get('password')
        print password
        user = authenticate(username=username, password=password)   #判断
        ret = {}
        if user is not None:    #用户存在
            login(request, user)  #登录
            ret['status'] = 0
        else:
            ret['status'] = 1
        print ret
        return JsonResponse(ret)


def mylogout(request):
    logout(request)
    return HttpResponseRedirect("login")
