# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View,ListView,DetailView, TemplateView
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from . import inception
# Create your views here.


class inception_commit(TemplateView):
    template_name = "inception_commit.html"
    def  post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        print(webdata)
        inception.table_structure(webdata['sqlcontent'])
        return JsonResponse({'status':0})


