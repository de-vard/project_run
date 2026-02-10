from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['athlete']  # ← вот это главное

    def get_queryset(self):

        queryset = Challenge.objects.all()

        athlete_id = self.request.query_params.get('athlete')
        if athlete_id:
            return queryset.filter(athlete_id=athlete_id)

        if self.request.user.is_authenticated:
            return queryset.filter(athlete=self.request.user)

        return Challenge.objects.none()

