# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import Note

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
