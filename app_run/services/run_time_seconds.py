from django.db.models import Min, Max
from datetime import timedelta


from app_run.models import Run


class RunTimeCalculator:
    """
    Сервис для расчёта времени забега на основе date_time позиций.
    Не зависит от порядка создания записей в БД.
    """

    def __init__(self, run: Run):
        self.run = run

    def calculate_run_time_seconds(self) -> int:
        """
        Возвращает длительность забега в секундах на основе самой ранней и самой поздней позиции.
        Если позиций недостаточно → возвращает 0.
        """
        if not self.run.positions.exists():
            return 0

        times = self.run.positions.aggregate(
            min_time=Min('date_time'),
            max_time=Max('date_time'),
        )

        min_time = times['min_time']
        max_time = times['max_time']

        if min_time is None or max_time is None or min_time >= max_time:
            return 0

        delta: timedelta = max_time - min_time
        return int(delta.total_seconds())

    @classmethod
    def update_run_time(cls, run: Run) -> None:
        """
        Удобный класс-метод: рассчитать и сразу сохранить в run.
        """
        calculator = cls(run)
        run.run_time_seconds = calculator.calculate_run_time_seconds()
        run.save(update_fields=['run_time_seconds'])