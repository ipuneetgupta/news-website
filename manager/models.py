from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Manager(models.Model):
    name = models.CharField(default=" ",max_length=200)
    u_name = models.CharField(default=" ",max_length=100)
    e_mail = models.TextField()
    
    def __str__(self):
        return self.u_name
