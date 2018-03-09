from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^inception_commit/$', inception_commit.as_view()),
    url(r'^dbconfig/(?P<pk>\d+)?/?$', dbconfig.as_view(), name='dbconfig'),
    url(r'^autoselect/$', autoselect.as_view(), name='autoselect'),
    url(r'^dbexe/(?P<pk>\d+)?/?$', dbexe.as_view(), name='dbexe'),
    url(r'^dbrollback/(?P<pk>\d+)?/?$', dbrollback.as_view(), name='dbrollback'),
]