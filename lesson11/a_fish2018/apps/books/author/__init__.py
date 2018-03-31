# coding = utf8
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from books.models import Author
from books.forms import AuthorForm
import json
import logging
logger = logging.getLogger('opsweb')



class AuthorListView(LoginRequiredMixin,PaginationMixin,ListView):

    model = Author
    template_name = "books/author_list.html"
    context_object_name = "author_list"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(AuthorListView,self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                       Q(address__icontains=self.keyword) |
                                       Q(phone__icontains=self.keyword)|
                                       Q(email__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self,request):
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code':0,'result':'success'}
        else:
            res = {'code':1,'errmsg':form.errors}
            print form.errors
        return JsonResponse(res,safe=True)


class AuthorDetailView(LoginRequiredMixin,DetailView):

    model = Author
    template_name = "books/author_detail.html"
    context_object_name = 'author'
    next_url = '/books/authorlist/'

    def post(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = AuthorForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
            res = {"code":0,"result":"success",'next_url':self.next_url}
        else:
            res = {"code":1,"errmsg":form.errors,'next_url':self.next_url}
        return render(request,settings.JUMP_PAGE,res)


    def delete(self,request,*args,**kwargs):
        pk = kwargs.get('pk')

        try:
            obj = self.model.objects.get(pk=pk)
            if not obj.book_set.all():
                self.model.objects.filter(pk=pk).delete()
                res = {"code":0,"result":"success"}
            else:
                res = {"code":1,"errmsg":"error"}
        except:
            res = {"code":1,"errmsg":"error"}
        return JsonResponse(res,safe=True)