from django.db import models

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    city = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'data'

class BaseCities(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_cities'


class BaseProvinces(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_provinces'

class Keyword(models.Model):
    key = models.CharField( max_length=50)
    data = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keyword'
class Regex(models.Model):
    zz = models.CharField(max_length=100, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regex'
