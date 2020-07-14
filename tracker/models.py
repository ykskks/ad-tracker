from django.db import models
from django.urls import reverse


# Create your models here.
class Advertiser(models.Model):
    id = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('home')


class Ad(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

