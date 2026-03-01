from django.contrib.auth.models import User
from rest_framework import serializers

from artifacts.models import CollectibleItem
from .models import Run, AthleteInfo


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор списка пользователя """
    type = serializers.SerializerMethodField()
    runs_finished = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'date_joined', 'username',
            'last_name', 'first_name', 'type',
            'runs_finished'
        ]

    def get_type(self, obj):
        return "coach" if obj.is_staff else "athlete"




class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ['id', 'name', 'uid', 'picture', 'value', 'latitude', 'longitude']


class UsersSerializerDetail(UsersSerializer):
    """Сериализатор детально просмотра пользователя """
    items = CollectibleItemSerializer(many=True, read_only=True)

    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields + ["items"]


class UserNestedSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для RunSerializer"""

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    """Сериализатор для сущностей бега и вывода пользователей"""
    athlete_data = UserNestedSerializer(source='athlete', read_only=True)
    speed = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class AthleteInfoSerializer(serializers.ModelSerializer):
    """Для дополнительной информации от пользователя"""

    class Meta:
        model = AthleteInfo
        fields = ['goals', 'weight', 'id']
        read_only_fields = ['id', ]
