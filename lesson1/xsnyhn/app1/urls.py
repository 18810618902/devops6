#coding=utf-8

from django.conf.urls import url
from app1.views import *
urlpatterns = [
    url(r'^hello', hello, ),
    url(r'^users/([0-9]{1,3}$)',users),  #(\d*)、(\d+ $)、(\w+) w包含数字和字符 (\d{1,3}$),一到三个数字
    url(r'^add/(\d{1,2})/(\d{1,2}$)',add,name='add'),  #隐式位置参数，在views函数的位置变量获取
    url(r'^users1/(?P<pk>\d+)',users1),  #通过字典的key值进行获取
    url(r'^argstest', argstest),
]
