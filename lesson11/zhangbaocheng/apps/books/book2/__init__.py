# coding=utf8
from django.views.generic.edit import CreateView
from books.models import Book,Author,Publish
from django.core.exceptions import ImproperlyConfigured
from books.forms import BookForm
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

class BookAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    增加
    """
    model = Book
    template_name = 'books/book_add.html'
    fields = ['name', 'publisher', 'authors', 'publication_date']
    success_message = 'Add %(name)s Successful'

    def  get_success_url(self):
        if '_addanother' in self.request.POST:
            return  reverse('books:book_add')
        return reverse('books:book_list')



    def get_context_data(self, **kwargs):
        self.keyword = self.request.GET.get('keyword', '').strip()
        context = super(BookAddView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context

