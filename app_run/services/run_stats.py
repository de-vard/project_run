from decimal import Decimal, ROUND_HALF_UP

from app_run.models import Run


class RunStatsService:
    @staticmethod
    def calculate_stats(run: Run):
        """Возвращает dict с актуальными статистиками по позициям"""
        positions = run.positions.order_by('date_time').all()

        if len(positions) < 2:
            return {
                'total_distance_km': Decimal('0.00'),
                'average_speed_ms': Decimal('0.00'),
            }

        # Общее расстояние — из последней позиции (это уже проверено, что считается верно)
        total_distance = positions.last().distance

        # Время — из поля модели (RunTimeCalculator должен быть верным)
        total_seconds = run.run_time_seconds or 0

        # Классическая средняя скорость = дистанция / время
        if total_seconds > 0:
            meters = total_distance * Decimal('1000')
            avg_speed = meters / Decimal(total_seconds)
            avg_speed = avg_speed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            avg_speed = Decimal('0.00')

        return {
            'total_distance_km': total_distance.quantize(Decimal('0.01')),
            'average_speed_ms': avg_speed,
        }