# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import os,django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
# django.setup()

from django.db import models

# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=32)
    note = models.TextField(null=True,blank=True)
    createtime = models.DateField(null=True,blank=True,auto_now_add=True)
    updatetime = models.DateField(null=True,blank=True,auto_now=True)

    class Meta:
        ordering = ['-id']
        abstract = True

    def __unicode__(self):
        return self.name

class Publish(BaseModel):
    city = models.CharField(max_length=32)

class Author(BaseModel):
    address = models.CharField(max_length=64,null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True)
    fans = models.IntegerField(null=True,blank=True)
    income = models.IntegerField(null=True,blank=True)


    @property
    def todict(self):
        include = ['address','phone','name']
        ret = dict()
        ret['books'] = [{'name':bk.name,'price':bk.price,'publish':bk.publish.name} for bk in self.book_set.all()]
        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self,fieldname)
            if fieldname not in include:continue
            if fieldname == 'phone':
                if fieldvalue and len(fieldvalue) == 11:
                    fieldvalue = fieldvalue[0:3] + '****' + fieldvalue[7:11]
            ret[fieldname] = fieldvalue
        return ret

class Book(BaseModel):
    price = models.IntegerField()
    publish = models.ForeignKey("Publish",null=True,blank=True)
    author = models.ManyToManyField("Author",null=True,blank=True)

    @property
    def priceplus(self):
        return self.price + 1

    @property
    def todict(self):
        include = ['name','note','price']
        ret = dict()
        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self,fieldname)
            if fieldname not in include:continue
            if fieldname == 'note':
                if fieldvalue and len(fieldvalue) > 5:
                    fieldvalue = fieldvalue[0:5] + '... ...'
            ret[fieldname] = fieldvalue
        return ret

