# -*- coding: utf-8 -*-
# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
# from django.http.response import JsonResponse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def firstpage(request):
    return render(request, 'index2.html')

def mylogin(request):
    if request.method == 'GET':
        return render(request,'pages/examples/login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        passwd = request.POST.get('passwd')
        user = authenticate(username=name, password=passwd)
        ret={}
        if user is not None:
            login(request,user)
            ret['status'] = 0
        else:
            ret['status'] = 1
        return JsonResponse(ret)

def mylogout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'mylogin'))
    # return HttpResponseRedirect(reverse("mylogin"))




