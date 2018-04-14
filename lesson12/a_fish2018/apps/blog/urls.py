from django.conf.urls import url
from blog.views import NoteDetailView

urlpatterns = [
    url(r'^note/(?P<pk>[0-9]+)?/$', NoteDetailView.as_view(), name='note'),
]
