from django.conf.urls import url,include
from django.contrib import admin
from app1.views import *
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$',firstpage.as_view(),name='firstpage'),
    url(r'^admin/', admin.site.urls),
    url(r'^app1/',include('app1.urls')),
    url(r'^login/$', RedirectView.as_view(url='/mylogin?next=/')),
    url(r'^mylogin$',mylogin.as_view(),name='mylogin'),
    url(r'^mylogout$',mylogout.as_view(),name='mylogout'),
    url(r'^bookquery/$',bookquery.as_view()),
    url(r'^authorquery/$',authorquery.as_view()),
    url(r'^users/$',users.as_view()),
    url(r'^authorlist/$',authorlist.as_view()),
    url(r'^users1/(?P<pk>\d+)',users1.as_view()),
    url(r'^hello/(?P<pm>\d+)',hello.as_view()),
]

