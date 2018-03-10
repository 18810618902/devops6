from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^inception_commit/$', inception_commit.as_view()),
    url(r'^inc_show/$', inc_show.as_view()),
    url(r'^inception_list/(?P<pk>\d+)?/?$', inception_list.as_view(),name='inception_list'),
    url(r'^dbconfig/(?P<pk>\d+)?/?$', dbconfig.as_view(), name='dbconfig'),
    url(r'^autoselect/', autoselect.as_view(), name='autoselect'),
]

