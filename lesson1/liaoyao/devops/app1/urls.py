from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bookquery$', views.bookquery,name='bookquery'),
    url(r'^authorquery$',views.authorquery,name='authorquery'),
    url(r'^hello/$',views.hello.as_view(), name='hello'),
    url(r'^authors/$', views.authorlist.as_view(),name='authorlist'),
]
