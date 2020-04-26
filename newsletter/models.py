from __future__ import unicode_literals
from django.db import models
# Create your models here.


class NewsLetter(models.Model):
    contactUserTxt = models.CharField(default=" ",max_length=50)
    isEmail = models.IntegerField(default=0)
    def __str__(self):
        return self.contactUserTxt
