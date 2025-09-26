from django.db import models
from django.contrib.auth.models import User

class Run(models.Model):
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
