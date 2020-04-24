from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Cat(models.Model):
    catName = models.CharField(default="#",max_length=300)
    newsCount = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.catName)+" | "+str(self.pk)
