from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from positions.models import Position
from positions.serializers import PositionSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run']


