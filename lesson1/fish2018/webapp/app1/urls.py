from django.conf.urls import url
from .views import hello,add,add2,add3,users,argstest

urlpatterns = [
    # url(r'^$', firstpage,name='home'),

    url(r'^hello/',hello,name='hello'),
    url(r'^argstest/',argstest,name='argstest'),
    url(r'^users/(?P<pk>\d+)',users,name='users'),
    url(r'^add/(\d+)/(\d+)',add,name='add'),
    url(r'^add/',add2,name='add2'),
    url(r'^addpost/',add3,name='add3'),
]