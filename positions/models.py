from django.core.validators import MinValueValidator
from django.utils import timezone

from django.db import models

from app_run.models import Run


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name='positions')
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    date_time = models.DateTimeField()
    speed = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
