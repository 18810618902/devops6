# coding=utf8
from django.views.generic.edit import CreateView
from books.models import Book,Author,Publish
from django.core.exceptions import ImproperlyConfigured
from books.forms import BookForm
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy


class BookAddView(CreateView):
    """
    增加
    """
    model = Book
    from_class = BookForm
    template_name = 'books/book_add.html'
    fields = ['name', 'publisher', 'authors', 'publication_date']
    success_url = '/books/booklist/'


    def form_invalid(self, form):
        return super(BookAddView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        self.keyword = self.request.GET.get('keyword', '').strip()
        context = super(BookAddView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context
