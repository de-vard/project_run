from django.db import models
from django.conf import settings


class CollectibleItem(models.Model):
    """Модель для артефактов которые можно собрать в забеге"""
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=50, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.IntegerField()
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collectible_items')
