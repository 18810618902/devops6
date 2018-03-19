from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from books.models import *
from books.forms import BookForm
import json
import logging
logger = logging.getLogger('opsweb')


from django.views.generic.edit import CreateView, UpdateView, DeleteView
class BookAddView(CreateView):
    model = Book
    template_name = "books/book_add.html"
    fields = ['name','publisher','authors','publication_date']


    def get_context_data(self, **kwargs):
        context = super(BookAddView, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context
