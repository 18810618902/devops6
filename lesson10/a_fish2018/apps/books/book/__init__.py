# coding = utf8
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

class BookListView(LoginRequiredMixin,PaginationMixin,ListView):

    model = Book
    template_name = "books/book_list.html"
    context_object_name = "book_list"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(BookListView,self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()

        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                       Q(authors__name__icontains=self.keyword) |
                                       Q(publisher__name__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context

    def post(self,request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code':0,'result':'success'}
        else:
            res = {'code':1,'errmsg':form.errors}
            print form.errors
        return JsonResponse(res,safe=True)

class BookDetailView(LoginRequiredMixin,DetailView):

    model = Book
    template_name = "books/book_detail.html"
    context_object_name = 'book'
    next_url = '/books/booklist/'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView,self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['publishs'] = Publish.objects.all()
        return context


    def post(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = BookForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
            res = {"code":0,"result":"success",'next_url':self.next_url}
        else:
            res = {"code":1,"errmsg":form.errors,'next_url':self.next_url}
        return render(request,settings.JUMP_PAGE,res)


    def delete(self,request,*args,**kwargs):
        pk = kwargs.get('pk')

        try:
            self.model.objects.filter(pk=pk).delete()
            res = {"code":0,"result":"success"}
        except:
            res = {"code":1,"errmsg":"error"}
        return JsonResponse(res,safe=True)