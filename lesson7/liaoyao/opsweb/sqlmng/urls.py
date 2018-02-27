from django.conf.urls import url
from . import  views







urlpatterns = [
    url('^inception_commit/$',views.inception_commit.as_view(),name='inception_commit'),
]