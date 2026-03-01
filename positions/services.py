# positions/services.py
from decimal import Decimal, ROUND_HALF_UP
from geopy.distance import geodesic
from django.utils import timezone


class PositionProcessor:
    def __init__(self, position: 'Position'):
        self.position = position
        self.run = position.run

    def process(self):
        """Вызывается после создания позиции"""
        if self.is_first_position():
            self.set_first_position_values()
        else:
            self.calculate_from_previous()

        self.position.save(update_fields=['distance', 'speed'])

    def is_first_position(self) -> bool:
        return not self.run.positions.exclude(pk=self.position.pk).exists()

    def set_first_position_values(self):
        self.position.distance = Decimal('0.00')
        self.position.speed = Decimal('0.00')

    def calculate_from_previous(self):
        prev = self.get_previous_position()

        # ── Расстояние между точками (в метрах) ────────────────
        point1 = (float(prev.latitude), float(prev.longitude))
        point2 = (float(self.position.latitude), float(self.position.longitude))
        segment_m = geodesic(point1, point2).meters

        # ── Время между точками (в секундах) ───────────────────
        time_delta = self.position.date_time - prev.date_time
        seconds = Decimal(time_delta.total_seconds())

        # ── Скорость на участке (м/с) ──────────────────────────
        if seconds > 0:
            speed_ms = Decimal(segment_m) / seconds
            speed_ms = speed_ms.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            speed_ms = Decimal('0.00')

        # ── Накопленное расстояние (км) ────────────────────────
        new_distance_km = prev.distance + Decimal(segment_m) / Decimal('1000')
        new_distance_km = new_distance_km.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        self.position.distance = new_distance_km
        self.position.speed = speed_ms

    def get_previous_position(self):
        return self.run.positions.filter(
            date_time__lt=self.position.date_time
        ).order_by('-date_time').first()