
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hello', hello),
    url(r'^users/(\d{1,3})$',users),
    url(r'^add/(\d{1,2})/(\d{1,2})$',add,name='add'),
    url(r'^users1/(?P<pk>\d+)',users1),
    url(r'argstest',argstest),     #http://192.168.64.146:9000/app1/argstest/?name=changhw&id=111

]

