#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.forms.models import model_to_dict
import datetime

# Create your models here.

class Basemodel(models.Model):
    '''
       基础表(抽象类)
    '''
    name = models.CharField(max_length=32, verbose_name='名字')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    note = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    def __unicode__(self):
        return self.name  # 显示对象的名字

    class Meta:
        abstract = True  # 抽象类
        ordering = ['-id']  # 按id倒排

class Book(Basemodel):
    '''
    图书表
    '''
    price = models.IntegerField()
    pub_date = models.DateField(default=datetime.date.today)
    clicknum = models.IntegerField(default=0, verbose_name='点击量')
    sellnum = models.IntegerField(default=0, verbose_name='销量')
    # 多对多关系，第三表会自动创建
    author = models.ManyToManyField("Author", null=True, blank=True)
    # 一对多关系
    publish = models.ForeignKey("Publish", null=True, blank=True)

    #class Meta:  # 子类重写了Meta，父类的Meta在此无效
        #verbose_name_plural = '图书'  # 显示表的名字（别名）

    def to_dict(self):
        return model_to_dict(self, exclude=['createtime'])

class Author(Basemodel):
    '''
    作者表
    '''
    phone = models.CharField(max_length=11, verbose_name='手机号码', null=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    fansnum = models.IntegerField(default=0, verbose_name='粉丝量')
    income = models.IntegerField(default=0, verbose_name='收入')

    @property
    def todict(self):
        ret = dict()
        include = ['id', 'name', 'phone', 'fansnum', 'income','address']  # 显示的字段
        #ret['books'] = [ {'name': i.get('name'), 'price':i.get('price')} for i in self.book_set.values()]
        #ret['books'] = [ {'id':bk.id, 'name':bk.name, 'price':bk.price, 'publish':bk.publish.name} for bk in self.book_set.all()]
        ret['books'] = [ {'id':bk.id, 'name':bk.name, 'price':bk.price} for bk in self.book_set.all()]

        for attr in [f.name for f in self._meta.fields]:
            attrvalue = getattr(self, attr)
            if attr not in include: continue
            if attr == 'note':
                if attrvalue:
                    attrvalue = attrvalue[0:5] + '***'
            elif attr == 'phone':
                if attrvalue:
                    attrvalue = attrvalue[0:3] + '****' + attrvalue[7:11]
            ret[attr] = attrvalue
        return ret

class Publish(Basemodel):
    '''
    出版社表
    '''
    city = models.CharField(max_length=32)

