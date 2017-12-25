from django.conf.urls import url,include
from django.contrib import admin
from app1.views import mylogin,firstpage

urlpatterns = [
    url(r'^$',firstpage,name='firstpage'),
    url(r'^admin/', admin.site.urls),
    url(r'^app1/',include('app1.urls')),
    url(r'^mylogin$',mylogin),
]
