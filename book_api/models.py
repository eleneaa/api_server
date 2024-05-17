from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list
    city = models.CharField(max_length=15)
    description = models.CharField(max_length=200)
    url = models.URLField()
    confirmed = models.BooleanField()
    occupied = models.BooleanField()
    last = models.BooleanField()
    class Meta:
        db_table = 'Book'
