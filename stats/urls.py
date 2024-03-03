# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import stats as stats_views

router = DefaultRouter()
router.register(r'dashboard', stats_views.DashBoardViewSet, basename='devices')


urlpatterns = [
    path('', include(router.urls)),
]
