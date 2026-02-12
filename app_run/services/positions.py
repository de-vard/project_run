from geopy.distance import geodesic



class NotEnoughPositions(Exception):
    """Выбрасывается, когда для расчёта дистанции недостаточно точек."""
    pass


class PositionService:
    """Вычисление пройденной дистанции по списку координат."""
    def __init__(self, run):
        self.run = run

    def get_distance(self) -> float:
        """Вычисление пройденной дистанции по списку координат."""
        positions = list(self.run.positions.order_by('id'))

        if len(positions) < 2:
            raise NotEnoughPositions("Not enough positions")

        total = 0.0
        for i in range(len(positions) - 1):
            p1 = (positions[i].latitude, positions[i].longitude)
            p2 = (positions[i + 1].latitude, positions[i + 1].longitude)
            total += geodesic(p1, p2).kilometers

        return total
