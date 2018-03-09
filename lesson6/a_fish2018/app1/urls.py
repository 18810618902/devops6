#coding=utf-8

from django.conf.urls import include, url
from .views import *
from  . import  book,author,publish

urlpatterns = [
    # class base view
    url(r'^authorlist/$', author.AuthorList.as_view(), name='authorlist'),
    url(r'^authordetail/(?P<pk>\d+)?/?$', author.AuthorDetail.as_view(), name='authordetail'),
    url(r'^authorapi/(?P<pk>\d+)?/?$', author.AuthorApi.as_view(), name='authorapi'),

    url(r'^booklist/$', book.BookList.as_view(), name='booklist'),
    url(r'^bookdetail/(?P<pk>\d+)?/?$', book.BookDetail.as_view(), name='bookdetail'),
    url(r'^bookapi/(?P<pk>\d+)?/?$', book.BookApi.as_view(), name='bookapi'),

    url(r'^publishlist/$', publish.PublishList.as_view(), name='publishlist'),
    url(r'^publishdetail/(?P<pk>\d+)?/?$', publish.PublishDetail.as_view(), name='publishdetail'),

]

