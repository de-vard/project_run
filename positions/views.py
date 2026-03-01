from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from app_run.services.collectibles import CollectibleService
from positions.models import Position
from positions.serializers import PositionSerializer
from positions.services import PositionProcessor


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run']

    def perform_create(self, serializer):
        position = serializer.save()

        # 1. Считаем distance и speed
        processor = PositionProcessor(position)
        processor.process()

        # 2. Обрабатываем коллекционные предметы (оставляем как было)
        CollectibleService(position).process()