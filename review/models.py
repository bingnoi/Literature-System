from django.db import models

# Create your models here.
class Submit(models.Model):
    username = models.CharField(max_length=32)
    qq = models.CharField(max_length=32)
    review = models.CharField(max_length=1000)