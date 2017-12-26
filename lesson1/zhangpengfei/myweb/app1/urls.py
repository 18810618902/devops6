#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'hello/',hello),
    # url(r'user/(\d+)$',user),
    url(r'user/(\d{1,3})$',user),
    url(r'add/(\d{1,3})/(\d{1,3})$',add,name='add'),  #name url反转
    url(r'users1/(?P<pk1>\d+)/(?P<pk2>\d+)$',users1),
    url(r'argstest',argstest),
]
