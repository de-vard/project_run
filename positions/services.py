# positions/services.py
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from geopy.distance import geodesic   # pip install geopy  (если ещё не установлен)

from positions.models import Position


class PositionProcessor:
    def __init__(self, position: Position):
        self.position = position
        self.run = position.run

    def process(self):
        """Вычисляем distance и speed для текущей позиции"""
        if not self.run.positions.exists():
            # Первая позиция
            self.position.distance = Decimal('0.00')
            self.position.speed = Decimal('0.00')
            self.position.save(update_fields=['distance', 'speed'])
            return

        # Берём предыдущую позицию (по времени — самую последнюю до текущей)
        prev = self.run.positions.exclude(id=self.position.id)\
                                .filter(date_time__lt=self.position.date_time)\
                                .order_by('-date_time')\
                                .first()

        if not prev:
            # Теоретически не должно быть, но на всякий случай
            self.position.distance = Decimal('0.00')
            self.position.speed = Decimal('0.00')
        else:
            # 1. Расстояние между двумя точками (в км)
            point1 = (float(prev.latitude), float(prev.longitude))
            point2 = (float(self.position.latitude), float(self.position.longitude))
            segment_km = Decimal(str(geodesic(point1, point2).km)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

            # 2. Накопленное расстояние
            self.position.distance = (prev.distance + segment_km).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

            # 3. Время между точками в секундах
            time_delta = self.position.date_time - prev.date_time
            seconds = Decimal(time_delta.total_seconds())

            # 4. Скорость м/с = метры / секунды
            if seconds > 0:
                meters = segment_km * Decimal('1000')
                speed_ms = meters / seconds
                self.position.speed = speed_ms.quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
            else:
                self.position.speed = Decimal('0.00')

        self.position.save(update_fields=['distance', 'speed'])

        # Опционально: обновить общее расстояние забега сразу (удобно для фронта)
        self._update_run_total_distance()

    def _update_run_total_distance(self):
        """Обновляем поле distance в модели Run (текущее значение)"""
        latest = self.run.positions.order_by('-date_time').first()
        if latest:
            self.run.distance = latest.distance
            self.run.save(update_fields=['distance'])