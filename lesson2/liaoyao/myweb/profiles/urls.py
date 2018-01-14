from django.conf.urls import url
from . import views








urlpatterns = [
    url(r'^$',views.index,name='profile_index'),
    url(r'^userinfo/(?P<user>\w+\d+)$',views.userinfo,name='userinfo'),
]
