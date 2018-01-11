# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
# Create your views here.



def index(request):
    return HttpResponse('index')



def userinfo(request,user):
    result = dict()
    result['data'] = dict()
    result['msg'] = 'userdata'
    try:
        res = User.objects.get(username=user)
        result['data']['address'] = res.userprofile.address.encode('utf-8')
        result['data']['phone'] = res.userprofile.phone
        result['data']['id'] = res.id
        result['data']['username'] = res.username
        result['status'] = 0
    except User.DoesNotExist:
        print('user is no exist')
        result['data'] = 'None'
        result['status'] = 1
    print(result)
    return JsonResponse(result)
