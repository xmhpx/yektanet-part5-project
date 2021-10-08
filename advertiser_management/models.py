from django.db import models


class Advertiser(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Ad(models.Model):
    def __str__(self):
        return self.title
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    imgUrl = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

# Create your models here.
