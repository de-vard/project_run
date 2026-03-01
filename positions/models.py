# positions/models.py
from django.core.validators import MinValueValidator
from django.db import models
from app_run.models import Run


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name='positions')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date_time = models.DateTimeField()

    # Новые поля
    speed = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Скорость м/с между предыдущей и текущей позицией"
    )
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Накопленное расстояние в км от начала забега до этой точки"
    )

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f"Pos {self.id} @ {self.date_time}"