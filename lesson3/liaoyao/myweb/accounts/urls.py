from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views



urlpatterns = [
    url(r'^$', login_required(views.index.as_view())),
    url(r'^mylogout', views.mylogout.as_view(),name='accounts_logout'),
    url(r'^mylogin$', views.mylogin.as_view(),name='accounts_login'),
    url(r'^authorquery$',views.authorquery.as_view(),name='accounts_authorquery'),
    url(r'^authorlist$',views.authorlist.as_view(),name='accounts_authorlist'),
]
