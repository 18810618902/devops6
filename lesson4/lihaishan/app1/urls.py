#coding=utf-8

from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^authorapi/(?P<pk>\d+)?/?$', authorapi.as_view()),
    url(r'^authorlist/(?P<pk>\d+)?/?$', authordetail.as_view(), name='authordetail'),

]

