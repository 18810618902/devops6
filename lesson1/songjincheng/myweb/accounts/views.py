# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import random
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def firtlogin(request):
    return HttpResponse("hello world!1111")

def users(request, pk):
    print pk
    # 链接数据库，获取PK的数据，转化下格式data
    return HttpResponse(pk)

def add(request, n1, n2):
    return HttpResponse(int(n1)+int(n2))

def user1(request, **kwargs):
    pk1 = kwargs.get('pk')
    # 链接数据库，获取PK的数据，转换下格式data
    return HttpResponse(pk1)


def argstest(request):
    name = request.GET.get("username")
    uid = request.GET.get("id")
    ret = {'name': name, 'id': uid}
    return JsonResponse(ret)
# ?username=xiaosong&password=123456


def hello(request):
    return render(request, 'accounts/hello.html', {'username': 'xiaosong'})


def wahaha(request):
    context = {}
    lans = ['python', 'golang']
    context['lans'] = lans
    context['username'] = 'xiaosong'
    users = [
        {'name': 'name1', 'id': 1},
        {'name': 'name2', 'id': 2},
        {'name': 'name3', 'id': 3},
    ]
    context['n1'] = random.randint(0, 99)
    context['n2'] = random.randint(0, 99)
    context['users'] = users
    return render(request, 'accounts/hello.html', context)
# login.html


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')

        msg = "用户名密码错误"
        context = {}
        context['msg'] = msg
        return render(request, "accounts/login.html", context)
    return render(request, "accounts/login.html")



# 2种方式：
def Login_Two(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        ret = {}
        if user is not None and user.is_active:
            login(request, user)
            ret['status'] = 0
        else:
            ret['status'] = 1
        return JsonResponse(ret)
    return render(request, "accounts/login.html")


@login_required
def loginout_view(request):
    logout(request)
    return redirect("/account/login/")

