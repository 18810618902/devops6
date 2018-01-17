from django.conf.urls import url, include
from django.contrib import admin

from app1.views import *

urlpatterns = [
    url(r'^hello/(?P<pm>\d+)$', hello.as_view()),
    url(r'^add/(\d{1,2})/(\d{1,2})$', ADD.as_view()),
    url(r'^plus/(\d{1,2})/(\d{1,2})$', plus.as_view(),name='plus'),
    url(r'^user1/(?P<pk>\d+)$', user1.as_view()),
    url(r'^argsrequest/$', argstest.as_view()),
    url(r'^bookquery/$', bookquery.as_view()),
    url(r'^authquery/$', authquery.as_view()),
    url(r'^authors/$', authorlist.as_view()),
]
