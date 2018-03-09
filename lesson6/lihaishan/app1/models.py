# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from django.core import serializers

# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(max_length=32)
    note=models.TextField(null=True,blank=True)
    createtime=models.DateField(null=True,blank=True,auto_now_add=True)
    updatetime=models.DateField(null=True,blank=True,auto_now=True)
    def __unicode__(self):
        return self.name


    class Meta:
        ordering=['id']
        abstract=True

class Book(BaseModel):
    price = models.IntegerField()
    publish = models.ForeignKey("Publish", null=True, blank=True)
    author = models.ManyToManyField("Author", null=True, blank=True)

    @property
    def priceplus(self):
        return self.price + 1

    @property
    def todict(self):
        include = ['name','note','price']
        ret = dict()
        ret['publish']=self.publish
        author = [{'name': author.name,'id':author.id} for author in self.author.all()]
        ret['author'] = author
        for attr in self._meta.fields:
            print self._meta.fields
            fieldname = attr.name
            fieldvalue = getattr(self, fieldname)
            if fieldname not in include:continue
            if fieldname == 'note':
                if fieldvalue and len(fieldvalue) > 5:
                    fieldvalue = fieldvalue[0:5] + '... ...'
            ret[fieldname] = fieldvalue
        return ret


class Publish(BaseModel):
    city = models.CharField(max_length=32)

class Author(BaseModel):
    address = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    fans = models.IntegerField(null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)

    @property
    def todict(self):
        include = ['name', 'address', 'phone']
        ret = dict()
        ret['books'] = [ {'id':bk.id,'name':bk.name, 'price':bk.price} for bk in self.book_set.all()]
        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self, fieldname)
            if fieldname not in include:continue
            if fieldname == 'phone':
                if fieldvalue and len(fieldvalue) == 11:
                    fieldvalue = fieldvalue[0:3] + '****' + fieldvalue[7:11]

            ret[fieldname] = fieldvalue
        return ret
        print ret
