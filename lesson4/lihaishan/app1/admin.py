# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app1.models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Publish)
admin.site.register(Author)