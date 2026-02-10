from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    """Сущность забега"""

    class Actions(models.TextChoices):
        """Выбор действия"""
        INIT = 'init'
        PROGRESS = 'in_progress'
        FINISHED = 'finished'

        @classmethod
        def get_max_length(cls):
            return max(len(choice.value) for choice in cls)

    status = models.CharField(
        max_length=Actions.get_max_length(),
        choices=Actions.choices,
        default=Actions.INIT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    distance = models.FloatField(blank=True, null=True)


class AthleteInfo(models.Model):
    """Для дополнительной информации от пользователя"""
    goals = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


