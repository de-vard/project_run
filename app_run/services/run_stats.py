from decimal import Decimal, ROUND_HALF_UP
from app_run.models import Run


class RunStatsService:
    @staticmethod
    def calculate_stats(run: Run):

        positions = run.positions.order_by('date_time').all()

        if len(positions) < 2:
            return {
                'total_distance_km': Decimal('0.00'),
                'average_speed_ms': Decimal('0.00'),
            }

        total_distance = positions.last().distance

        speeds = [p.speed for p in positions if p.speed is not None]

        if speeds:
            avg_speed = sum(speeds) / Decimal(len(speeds))
            avg_speed = avg_speed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            avg_speed = Decimal('0.00')

        return {
            'total_distance_km': total_distance.quantize(Decimal('0.01')),
            'average_speed_ms': avg_speed,
        }