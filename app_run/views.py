from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.models import Run
from app_run.serializers import RunSerializer, UsersSerializer


@api_view(['GET'])
def company_details(request):
        details = {
            'company_name': settings.COMPANY_NAME,
            'slogan': settings.SLOGAN,
            'contacts': settings.CONTACTS
        }
        return Response(details)

class RunViewSet(viewsets.ModelViewSet):
    """Возвращаем сущность забегов"""
    serializer_class = RunSerializer

    # для оптимизации запросов к БД, решаем проблему с n+1
    queryset = Run.objects.all().select_related('athlete')

    # queryset = Run.objects.all()


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращение пользователей по параметру"""
    serializer_class = UsersSerializer

    def _check_parameter(self):
        """Проверка параметров"""
        pr = self.request.query_params.get("type", None)
        pr = pr if pr in ["coach", "athlete"] else None
        return pr

    @staticmethod
    def _is_coach(pr):
        """ Так как идет речь только об теренеров и подопечных,
            можно сравнить только на одно значение, выбор пал на тренера,
            если парамерт неравен coach значит он атлет
        """
        return pr == "coach"


    def get_queryset(self):
        """Переопределяем квэрисетов"""
        queryset = (User.objects.all().exclude(is_superuser=True))
        parameter = self._check_parameter()
        staff = self._is_coach(parameter)
        return queryset if not parameter else queryset.filter(is_staff=staff)
