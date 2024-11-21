from os import name
from django.db import models


# Create your models here.
class CountdownDate(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
