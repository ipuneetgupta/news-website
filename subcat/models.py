from __future__ import unicode_literals
from django.db import models
# Create your models here.


class SubCat(models.Model):
    subcatName = models.CharField(max_length=300)
    catName = models.CharField(max_length=300)
    catId = models.IntegerField(default=0)

    
    def __str__(self):
        return str(self.subcatName)+" | " + str(self.pk)
