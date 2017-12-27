# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    #url(r'^$',firstpage),
    url(r'^hello', hello, name="hello"),
    # 隐式位置参数
    url(r'users/(\d{1,3})$', users),
    url(r'^add/(\d{1,2})/(\d{1,2})/$', add, name="add"),
    # 显式位置参数
    url(r'^users1/(?P<pk>\d+)/(?P<pk1>\d{1,3})', users1), #http://0.0.0.0:9000/app1/argstest/?name=nick&id=123
    # 关键字参数
    url(r'^argstest', argstest),
]