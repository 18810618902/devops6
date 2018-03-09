#coding=utf-8

from django.conf.urls import include, url
from .views import *

urlpatterns = [
    # class base view
    url(r'^authorlist/$', AuthorList.as_view(), name='authorlist'),
    url(r'^authorapi/(?P<pk>\d+)?/?$', AuthorApi.as_view(), name='authorapi'),
    url(r'^authordetail/(?P<pk>\d+)?/?$', AuthorDetail.as_view(), name='authordetail'),
    #url(r'^booklist/(?P<pk>\d+)?/?$', BookList.as_view(), name='booklist'),

    url(r'^booklist/(?P<pk>\d+)?/?$', BookDetail.as_view(), name='bookdetail'),
    url(r'^bookapi/(?P<pk>\d+)?/?$', BookApi.as_view(), name='bookapi'),
]

