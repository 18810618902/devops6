from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.userlogin, name='login'),
    url(r'^logout/$', views.userlogout, name='logout')

]
