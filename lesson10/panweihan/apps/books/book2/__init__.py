# coding=utf8
from django.views.generic import View,TemplateView,ListView, DetailView,CreateView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.conf import settings
from books.models import Publish, Author, Book
from books.forms import PublishForm,AuthorForm,BookForm

import json
import logging


# class BookAddView(TemplateView):
#     template_name = "books/book_add.html"
class BookAddView(LoginRequiredMixin,CreateView):
    model = Book
    template_name = "books/book_add.html"
    context_object_name = 'book'
    fields = "__all__"
    next_url = '/books/booklist/'

    def get_context_data(self, **kwargs):
        context = super(BookAddView, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context

    # 利用中简页进行信息提示
    # def post(self, request,):
    #     form = BookForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         if '_addanother' in self.request.POST:
    #             next_url = '/books/bookadd/'
    #         else:
    #             next_url = '/books/booklist/'
    #         res = {"code": 0, "message": "添加图书成功", 'next_url':next_url}
    #     else:
    #         # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
    #         res = {"code": 1, "errmsg": form.errors, 'next_url': self.next_url}
    #     return render(request, settings.JUMP_PAGE, res)


    # 利用message进行信息提示
    def post(self, request,*args, **kwargs):
        super(BookAddView, self).post(request, *args, **kwargs)
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # 设置成功后跳转的地址
    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('books:book_add')
        return reverse('books:book_list')
