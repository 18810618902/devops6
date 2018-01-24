# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from  django.contrib.auth.models   import User
# Create your models here.

class BaseBook(models.Model):
    name = models.CharField(max_length=12,default="")
    note = models.TextField(null=True, blank=True)
    createtime = models.DateField(null=True, blank=True,auto_now_add =True)
    updatetime = models.DateField(null=True, blank=True ,auto_now=True)
    def __unicode__(self):
        return  self.name

    class  Meta:
        ordering = ["-id"]
        abstract = True


class Publish(BaseBook):
    city = models.CharField(max_length=32)

class Author(BaseBook):
    address = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    fans = models.CharField(max_length=12,null=True, blank=True)
    income = models.CharField(max_length=12,null=True, blank=True)

    @property
    def todict(self):
        include = ["name", "address", "phone","fans","income"]
        ret = dict()
        ret['book'] = [{"name":bk.name, 'price':bk.price,"publish": bk.publish.name}for bk in  self.book_set.all()]

        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self, fieldname)
            if fieldname not  in include:continue
            if fieldname  == "phone":
                if fieldvalue and  len(fieldvalue) == 11:
                    fieldvalue = fieldvalue[0:3] + "****" + fieldvalue[7:10]
            ret[fieldname] = fieldvalue
        return ret



class  Book(BaseBook):
    price = models.IntegerField(default="")
    publish = models.ForeignKey("Publish", null=True, blank=True,)
    author = models.ManyToManyField("Author", null=True, blank=True)

    def  priceplus(self):
        return  self.price + 1

    @property
    def todict(self):
        include = ["name", "note","createtime","updatetime"]
        ret = dict()
        for  attr in  self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self, fieldname)
            if fieldname in include:
                if fieldname == 'note':
                    if fieldvalue and len(fieldvalue) >0:
                        fieldvalue = "隐私内容*******请勿窥探"
                ret[fieldname] = fieldvalue
        return  ret