from geopy.distance import geodesic
from artifacts.models import CollectibleItem


class CollectibleService:
    def __init__(self, position):
        self.position = position
        self.athlete = position.run.athlete

    def process(self):
        athlete_point = (
            self.position.latitude,
            self.position.longitude
        )

        items = CollectibleItem.objects.all()

        for item in items:
            item_point = (item.latitude, item.longitude)
            distance = geodesic(athlete_point, item_point).meters

            if distance <= 100:
                item.user.add(self.athlete)
