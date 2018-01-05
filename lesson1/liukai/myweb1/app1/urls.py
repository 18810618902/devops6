from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hello/$', hello),
    url(r'^users/(\d+)', users),
    url(r'^add/(\d{1,2})/(\d+)$', add, name='add'),
    url(r'^users1/(?P<pk>\d+)', user1, name='user1'),
    url(r'^users2/(?P<pk1>\d+)/(?P<pk2>\d+)', user2, name='user2'),
    url(r'^argstest', argstest, name='argstes'),
]
