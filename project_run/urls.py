from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_run.views import company_details, RunViewSet, UsersViewSet, StartFiAPIView, StopFiAPIView, AthleteInfoAPIView
from artifacts.views import CollectibleItemViewSet, UploadExcelData
from challenges.views import ChallengeViewSet

from positions.views import PositionViewSet
from project_run import settings

router = DefaultRouter()
router.register('api/runs', RunViewSet)
router.register('api/positions', PositionViewSet)
router.register('api/collectible_item/', CollectibleItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', company_details),

    path('api/runs/<int:run_id>/start/', StartFiAPIView.as_view()),
    path('api/runs/<int:run_id>/stop/', StopFiAPIView.as_view()),

    path('api/athlete_info/<int:user_id>/', AthleteInfoAPIView.as_view()),
    path('api/users/', UsersViewSet.as_view({'get': 'list'})),

    path('api/challenges/', ChallengeViewSet.as_view({'get': 'list'})),

    path('api/upload_file/', UploadExcelData.as_view()),

    path('', include(router.urls)),

]

if settings.base.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
