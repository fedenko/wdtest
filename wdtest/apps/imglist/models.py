from django.db import models
from django.conf import settings

UPLOAD_TO = getattr(settings, "UPLOAD_IMAGES_DIR", "img")


class ImageList(models.Model):
    title = models.CharField(max_length=255, unique=True)
    creator_ip = models.IPAddressField(blank=True, null=True)

    def __unicode__(self):
        return self.title

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=UPLOAD_TO)
    lists = models.ManyToManyField(ImageList, related_name="images", blank=True, null=True)

    def __unicode__(self):
        return self.title
