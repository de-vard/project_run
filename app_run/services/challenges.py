from django.db.models import Count, Sum

from app_run.models import Run
from challenges.models import Challenge


class ChallengeService:
    """Проверка условий и выдача наград (достижений) атлету."""
    def __init__(self, athlete):
        self.athlete = athlete

    def apply_finished_run_challenges(self):
        """ Выполняется после каждого завершённого забега.
            Проверяет суммарную дистанцию и количество забегов,
            при выполнении условий создаёт соответствующее достижение.
            get_or_create гарантирует, что достижение не задвоится.
        """
        stats = Run.objects.filter(
            athlete=self.athlete,
            status=Run.Actions.FINISHED
        ).aggregate(
            total_sum=Sum('distance'),
            total_count=Count('id')
        )

        if stats['total_sum'] and stats['total_sum'] > 50:
            Challenge.objects.get_or_create(
                athlete=self.athlete,
                full_name=self.full_name_50
            )

        if stats['total_count'] >= 10:
            Challenge.objects.get_or_create(
                athlete=self.athlete,
                full_name=self.full_name_10
            )
