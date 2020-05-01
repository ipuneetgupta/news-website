from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Manager(models.Model):
    name = models.CharField(default="",max_length=200)
    u_name = models.CharField(default="",max_length=100)
    e_mail = models.TextField()
    user_ip = models.CharField(max_length=15,default="")
    user_ip = models.TextField(default="")
    country = models.CharField(default="",max_length=100)
    def __str__(self):
        return self.u_name
