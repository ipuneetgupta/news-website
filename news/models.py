from __future__ import unicode_literals
from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
# Create your models here.


class News(models.Model):

    title = models.CharField(default=None,max_length=500,null=True,blank=True)
    newsSummary = models.TextField(null=True,blank=True)
    newsContent = models.TextField(null=True,blank=True)
    newsImageUrl = models.ImageField(null=True,blank=True)
    image_url = models.URLField(null=True,blank=True)
    newsImageName = models.CharField(max_length=300,null=True,blank=True)
    publishDate = models.CharField(default=None,max_length=300,null=True,blank=True)
    writerName = models.CharField(default=None,max_length=300,null=True,blank=True)
    catName = models.CharField(default=None,max_length=300,null=True,blank=True)
    catId = models.IntegerField(default=0,null=True,blank=True)
    views = models.IntegerField(default=0,null=True,blank=True)
    ocatId = models.IntegerField(default=0,null=True,blank=True)
    tag = models.TextField(default=None,max_length=300,null=True,blank=True)
    act = models.IntegerField(default=0,null=True,blank=True)
    publisherName = models.CharField(default=None,max_length=300,null=True,blank=True)
    rand = models.IntegerField(default=0,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if self.image_url and not self.newsImageUrl:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.newsImageUrl.save(f"image_{self.pk}.jpeg", File(img_temp))
            self.newsImageUrl = self.newsImageUrl.url
            self.newsImageName = str(self.newsImageUrl)[7:]
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
