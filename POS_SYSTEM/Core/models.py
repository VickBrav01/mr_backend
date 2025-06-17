from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class BusinessDetails(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name
