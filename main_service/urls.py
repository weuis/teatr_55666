from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main_service.views import (
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    TheaterHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TicketViewSet
)

app_name = "main_service"

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genre')
router.register('actors', ActorViewSet, basename='actor')
router.register('plays', PlayViewSet, basename='play')
router.register('theater-halls', TheaterHallViewSet, basename='theater-hall')
router.register('performances', PerformanceViewSet, basename='performance')
router.register('reservations', ReservationViewSet, basename='reservation')
router.register('tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
