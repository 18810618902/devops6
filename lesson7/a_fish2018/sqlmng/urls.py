from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^inception_commit/$',inception_commit.as_view()),
]