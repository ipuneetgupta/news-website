from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Main(models.Model):
    name = models.CharField(default="#",max_length=100)
    about = models.TextField()
    fb = models.CharField(default="#", max_length=300)
    tw = models.CharField(default="#", max_length=300)
    yt = models.CharField(default="#", max_length=300)
    lk = models.CharField(default="#", max_length=300)
    vm = models.CharField(default="#", max_length=300)
    tel = models.CharField(default="#", max_length=10)
    mylink = models.CharField(default="#", max_length=300)
    site_name = models.CharField(default="#", max_length=300)

    def __str__(self):
        return self.site_name+" | "+str(self.pk)
