# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
import  random

# Create your views here.

def hello(request):
   #return HttpResponse("hello django")
   lans = ['python', 'java', 'go', 'ruby']
   users = [
       {'name': 'zhai' , 'id':1},
       {'name': 'liang' , 'id': 2},
       {'name': 'leon' , 'id': 3 },
   ]
   context = {}
   context['username'] = 'kingleoric'
   context['lans'] = lans
   context['users'] = users
   context['n1'] = random.randint(0,99)
   context['n2'] = random.randint(0,99)
   #print context
   return render(request, 'hello.html', context)
"""
def users(request, **kwargs):
    pk1 = kwargs.get('pk')
    print pk1
    return HttpResponse(pk1)
"""

def add(request,n1, n2):
    return HttpResponse(int(n1)+int(n2))

def argstest(request):
    name = request.GET.get('username')
    uid = request.GET.get('id')
    ret = {'name':name, 'id':uid}
    return JsonResponse(ret)