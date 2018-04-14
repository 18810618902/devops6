# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from blog.models import Note


# Create your views here.
class NoteDetailView(DetailView):
    template_name = 'note.html'
    context_object_name = 'note'
    model = Note

    def get_context_data(self, **kwargs):
        id = self.get_object().id
        context = super(NoteDetailView, self).get_context_data(**kwargs)
        context['note'] = self.model.objects.get(id=id)
        return context


from haystack.forms import SearchForm
from django.shortcuts import render
def full_search(request):
    sform = SearchForm(request.GET)
    return render(request,'search/s.html',{'form':sform})


