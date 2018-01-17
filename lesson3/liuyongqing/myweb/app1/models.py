# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# class Music(models.Model):
#     first_name=models.CharField(max_length=30)
#     last_name=models.CharField(max_length=30)
# class Album(models.Model):
#     artist=models.ForeignKey(Music,on_delete=models.CASCADE)
#     name=models.CharField(max_length=30)
#     num_stars=models.IntegerField()

# class Book(models.Model):
#     name = models.CharField(max_length=32)
#     price = models.IntegerField()
#     pub_date = models.DateField()
#     def __unicode__(self): # 在 Python3 用__str__代替__unicode__
#         return self.name


class BaseModel(models.Model):
    name=models.CharField(max_length=32)
    note=models.TextField(null=True,blank=True)
    createtime=models.DateField(null=True,blank=True,auto_now_add=True)
    updatetime=models.DateField(null=True,blank=True,auto_now=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['-id']
        abstract=True

class Publish(BaseModel):
    city=models.CharField(max_length=32)


class Author(BaseModel):
    phone=models.CharField(max_length=11,null=True,blank=True)
    address=models.CharField(max_length=32,null=True,blank=True)
    fans=models.IntegerField(null=True,blank=True)
    income=models.IntegerField(null=True,blank=True)


    @property
    def todict(self):
        include=['name','address','phone']
        ret={}
        ret['book'] = [ {'bookname': bk.name,'price':bk.price,'publish':bk.publish.name
                         } for bk in self.book_set.all()]
        for attr in self._meta.fields:
            fieldname=attr.name
            fieldvalue=getattr(self,fieldname)
            if fieldname not in include:continue
            if fieldname == 'phone':
                if fieldvalue and len(fieldvalue) == 11:
                    fieldvalue = fieldvalue[0:4] + '隐藏四位' + fieldvalue[7:]
            ret[fieldname]=fieldvalue
        return ret


class Book(BaseModel):
    price=models.IntegerField()
    publish=models.ForeignKey(Publish,null=True,blank=True)
    author=models.ManyToManyField(Author,null=True,blank=True)


    @property
    def priceplus(self):
        return self.price + 1

    @property
    def todict(self):
        inclde=['name','note']
        ret={}

        for attr in self._meta.fields:
            print(attr.name)
            fieldname=attr.name
            fieldvalue=getattr(self,fieldname)
            if fieldname in inclde:
                if fieldname == 'note':
                    if fieldvalue and fieldvalue > 5:
                        fieldvalue=fieldvalue[0:5] + '隐藏四位'+ fieldvalue[9:]
                ret[fieldname]=fieldvalue
                ret[fieldname] = fieldvalue

        return ret