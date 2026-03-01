# app_run/services/run_stats.py
from decimal import Decimal, ROUND_HALF_UP

from app_run.models import Run
from app_run.services.run_time_seconds import RunTimeCalculator


class RunStatsService:
    @staticmethod
    def calculate_average_speed(run: Run) -> Decimal:
        """ Вычисляет среднюю скорость забега в метрах в секунду.
            Округляет до двух знаков после запятой.
        """
        if run.distance <= 0:
            return Decimal('0.00')

        total_seconds = RunTimeCalculator.get_run_duration_seconds(run)
        if total_seconds <= 0:
            return Decimal('0.00')

        meters = Decimal(run.distance) * Decimal('1000')
        speed_ms = meters / Decimal(total_seconds)
        return speed_ms.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
