from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hello', hello,name='hello'),
    url(r'^user/(\d+)',user),
    url(r'^add/(\d{1,2})/(\d{1,2})$',add),
    url(r'^users/(?P<res>\d+)/(?P<ok>\d+)',users),
    url(r'^artest', artest),
]