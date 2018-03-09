# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  django.http import  JsonResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.views.generic import  View,ListView, TemplateView



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"