from django.conf.urls import url
from app1 import views
urlpatterns = [
    url(r'^hello/', views.hello),
    url(r'^user1/', views.user1),
    url(r'^users/(\d+)', views.users),
    url(r'^add/(\d+)/(\d+)', views.add,name='add'),
    url(r'^argstest/', views.argstest),
]
