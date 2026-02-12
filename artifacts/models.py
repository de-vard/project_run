import uuid

from django.db import models


class CollectibleItem(models.Model):
    """Модель для артефактов которые можно собрать в забеге"""
    name = models.CharField(max_length=200)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    latitude = models.DecimalField()
    longitude = models.DecimalField()
    picture = models.URLField()
    value = models.IntegerField()
