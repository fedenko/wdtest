from django.db import models
from django.conf import settings

UPLOAD_TO = getattr(settings, "UPLOAD_IMAGES_DIR", "img")


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=UPLOAD_TO)

    def __unicode__(self):
        return self.title


class ImageList(models.Model):
    title = models.CharField(max_length=255, unique=True)
    creator_ip = models.IPAddressField(blank=True, null=True)
    images= models.ManyToManyField(Image, related_name="lists")

    def __unicode__(self):
        return self.title
