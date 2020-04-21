from __future__ import unicode_literals
from django.db import models
# Create your models here.


class News(models.Model):
    name = models.CharField(default="#",max_length=300)
    short_txt = models.TextField()
    body_txt = models.TextField()
    pic = models.TextField()
    date = models.CharField(default="#",max_length=10)
    writer = models.CharField(default="#",max_length=50)

    def __str__(self):
        return self.name
