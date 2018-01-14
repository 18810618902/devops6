from django.db import models

# Create your models here.

"""
class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField()


    def __unicode__(self):
        return self.name
"""


class BaseModel(models.Model):
    name = models.CharField(max_length=32)
    note = models.TextField(null=True, blank=True)
    createtime = models.DateField(null=True,blank=True,auto_now_add=True)
    updatetime = models.DateField(null=True,blank=True,auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        abstract = True

class Book(BaseModel):
    price = models.IntegerField()

    @property
    def priceplus(self):
        return self.price+1

    @property
    def todict(self):
        for attr in self._meta.fields:
            fieldname = attr.name
            print(fieldname, getattr(self, fieldname))
