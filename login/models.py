from django.db import models

# Create your models here.
#coding:utf-8
from django.db import models

# Create your models here.

class Register(models.Model):
   username = models.CharField(max_length = 32,verbose_name = '用户名')
   password = models.CharField(max_length = 32,verbose_name = '密码')
   email = models.EmailField(verbose_name = '注册邮箱')
   phone_number = models.CharField(max_length = 14,verbose_name = '电话号码')

