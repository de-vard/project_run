import uuid

from django.db import models


class CollectibleItem(models.Model):
    """Модель для артефактов которые можно собрать в забеге"""
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=50, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.IntegerField()
