from rest_framework import serializers

from positions.models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['run', 'latitude', 'longitude']

    def validate_run(self, value):
        if value.status != "in_progress":
            raise serializers.ValidationError(
                "Нельзя передавать координаты для забега не в статусе in_progress."
            )
        return value

    def validate_latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise serializers.ValidationError(
                "Широта должна быть в диапазоне от -90 до 90."
            )
        return value

    def validate_longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise serializers.ValidationError(
                "Долгота должна быть в диапазоне от -180 до 180."
            )
        return value
