from rest_framework import serializers

from artifacts.models import CollectibleItem


class CollectibleItemSerializer(serializers.ModelSerializer):

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("value must be >= 0")
        return value

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("latitude out of range")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("longitude out of range")
        return value

    class Meta:
        model = CollectibleItem
        fields = '__all__'

