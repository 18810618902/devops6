from django.conf.urls import url, include
from django.contrib import admin

from app1.views import *

urlpatterns = [
    url(r'^hello/$', hello,name='hello'),
    url(r'^user/(\d+)$', users),
    url(r'^add/(\d{1,2})/(\d{1,2})$', ADD),
    url(r'^plus/(\d{1,2})/(\d{1,2})$', plus,name='plus'),
    url(r'^user1/(?P<pk>\d+)$', user1),
    url(r'^argsrequest/$', argstest),
]
