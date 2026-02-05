from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets, views, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

from app_run.models import Run, AthleteInfo, Challenge
from app_run.serializers import RunSerializer, UsersSerializer, AthleteInfoSerializer, ChallengeSerializer


class RunPagination(PageNumberPagination):
    """Класс пагинации"""
    # page_size = 5
    # max_page_size = 50
    page_size_query_param = 'size'  # Разрешаем изменять количество объектов через query параметр size в url


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
    # Указываем какой класс будет использоваться для фильтра и для сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']  # Поля, по которым будет происходить фильтрация
    ordering_fields = ['created_at']  # Поля по которым будет возможна сортировка
    pagination_class = RunPagination


class StartFiAPIView(views.APIView):
    """Изменяем статус, что забег продолжается """

    def post(self, request, run_id):
        obj = get_object_or_404(Run, id=run_id)

        if obj.status != Run.Actions.INIT:
            return Response(
                {'error': f'Cannot start run from {obj.status} status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.status = Run.Actions.PROGRESS
        obj.save()

        data = {
            'id': obj.id,
            'status': obj.status,
            'message': 'Run started successfully'
        }
        return Response(data, status=status.HTTP_200_OK)


class StopFiAPIView(views.APIView):
    """Изменяем статус, что забег закончился """

    def post(self, request, run_id):
        obj = get_object_or_404(Run, id=run_id)

        if obj.status != Run.Actions.PROGRESS:
            return Response(
                {'error': f'Cannot start run from {obj.status} status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.status = Run.Actions.FINISHED
        obj.save()

        count_finished = Run.objects.filter(status='finished').count()

        if count_finished == 10:
            challenger = Challenge()
            challenger.athlete = request.user
            challenger.full_name = "Сделай 10 Забегов!"
            challenger.save()

        data = {
            'id': obj.id,
            'status': obj.status,
            'message': 'Run started successfully'
        }
        return Response(data, status=status.HTTP_200_OK)


class AthleteInfoAPIView(views.APIView):
    """Для дополнительной информации от пользователя"""

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        obj, _ = AthleteInfo.objects.get_or_create(user=user)
        data = {
            'user_id': obj.user.id,
            'goals': obj.goals,
            'weight': obj.weight
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        data = {
            'user': user,
            'id': user.id,
            'goals': request.data['goals'],
            'weight': request.data['weight'],
        }

        weight = request.data.get('weight')
        if weight.isalpha():
            return Response({'error': 'Invalid weight'}, status=status.HTTP_400_BAD_REQUEST)
        if weight is not None and not (0 < int(weight) < 900):
            return Response({'error': 'Invalid weight'}, status=status.HTTP_400_BAD_REQUEST)

        obj, _ = AthleteInfo.objects.update_or_create(user=user)
        serializer = AthleteInfoSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status=status.HTTP_201_CREATED)


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращение пользователей по параметру"""
    serializer_class = UsersSerializer
    filter_backends = [SearchFilter, OrderingFilter]  # Подключаем SearchFilter
    search_fields = ['first_name', 'last_name']  # Указываем поля по которым будет вестись поиск
    ordering_fields = ['date_joined']  # Поля по которым будет возможна сортировка
    pagination_class = RunPagination

    def _check_parameter(self):
        """Проверка параметров"""
        pr = self.request.query_params.get("type", None)
        pr = pr if pr in ["coach", "athlete"] else None
        return pr

    @staticmethod
    def _is_coach(pr):
        """ Так как идет речь только об тренеров и подопечных,
            можно сравнить только на одно значение, выбор пал на тренера,
            если параметр неравен coach значит он атлет
        """
        return pr == "coach"

    def get_queryset(self):
        """Переопределяем квэрисет"""
        queryset = (User.objects.all().exclude(is_superuser=True))
        parameter = self._check_parameter()
        staff = self._is_coach(parameter)
        return queryset if not parameter else queryset.filter(is_staff=staff)


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['athlete_id']  # Указываем поля по которым будет вестись поиск
