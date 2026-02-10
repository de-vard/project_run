from django.db import models
from django.contrib.auth.models import User


class Challenge(models.Model):
    """Модель для челленджей"""
    full_name = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
