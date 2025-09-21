from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Run

class UsersSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        return "coach" if obj.is_staff else "athlete"

class UserNestedSerializer(serializers.ModelSerializer):
    """Вложеный сериализатор для  RunSerializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']

class RunSerializer(serializers.ModelSerializer):
    """Сериализатор для сущностей бега и вывода пользователей"""
    athlete_data = UserNestedSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
