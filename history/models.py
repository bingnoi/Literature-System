from django.db import models

# Create your models here.
#存储浏览记录
class user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    history = models.CharField(max_length=32)