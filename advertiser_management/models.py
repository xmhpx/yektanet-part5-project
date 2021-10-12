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


class Click(models.Model):
    def __str__(self):
        return "user with ip \"%s\" clicked on \"%s\" at \"%s\"" % (self.user_ip, self.ad, self.datetime)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    user_ip = models.GenericIPAddressField()


class View(models.Model):
    def __str__(self):
        return "user with ip \"%s\" viewed \"%s\" at \"%s\"" % (self.user_ip, self.ad, self.datetime)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    user_ip = models.GenericIPAddressField()


# Create your models here.
