from __future__ import unicode_literals
from django.db import models
# Create your models here.


class News(models.Model):
    title = models.CharField(default="#",max_length=300)
    newsSummary = models.TextField()
    newsContent = models.TextField()
    newsImageUrl = models.ImageField()
    newsImageName = models.CharField(default="#",max_length=300)
    publishDate = models.CharField(default="#",max_length=20)
    writerName = models.CharField(default="#",max_length=50)
    catName = models.CharField(default="#",max_length=100)
    catId = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
