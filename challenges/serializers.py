from rest_framework import serializers

from challenges.models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['full_name', 'athlete']
        read_only_fields = ['full_name', 'athlete']
