from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^hello', hello),
    #url(r'^users/(?P<pk>\d+)', users),
    url(r'add/(\d{1,2})/(\d{1,2})$', add, name='add'),
    url(r'^argstest',argstest),
]