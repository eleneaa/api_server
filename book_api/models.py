from django.conf import settings
from django.db import models


class Book(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    city = models.CharField(max_length=15)
    description = models.CharField(max_length=200)
    occupied = models.BooleanField()
    active = models.BooleanField()
    class Meta:
        db_table = 'Book'
