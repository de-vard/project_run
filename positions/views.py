from rest_framework import viewsets

from positions.models import Position
from positions.serializers import PositionSerializer


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
