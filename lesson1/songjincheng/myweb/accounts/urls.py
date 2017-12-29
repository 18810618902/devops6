# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from accounts.views import firtlogin, users, add, user1, argstest,hello
from accounts.views import Login, loginout_view

urlpatterns = [
    url(r'^login/$', Login, name='login'),
    url(r'^logout/$', loginout_view, name='logout'),
]