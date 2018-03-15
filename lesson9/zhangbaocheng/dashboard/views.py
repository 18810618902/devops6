# -*- coding: utf-8 -*-
from django.shortcuts import render,reverse

# Create your views here.
from django.contrib.auth.decorators import login_required
from  django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

class indextestView(LoginRequiredMixin,TemplateView):
    template_name = 'indextest.html'
