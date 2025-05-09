from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teatr_service.views import (
    GatunekViewSet,
    AktorViewSet,
    SztukaViewSet,
    SalaTeatralnaViewSet,
    PrzedstawienieViewSet,
    RezerwacjaViewSet,
    BiletViewSet
)

app_name = "teatr_service"


router = DefaultRouter()

router.register('gatunek', GatunekViewSet, basename='gatunek')
router.register('aktor', AktorViewSet, basename='aktor')
router.register('sztuka', SztukaViewSet, basename='sztuka')
router.register('sala_teatralna', SalaTeatralnaViewSet, basename='sala-teatralna')
router.register('przedstwa', PrzedstawienieViewSet, basename='pzedstwa')
router.register('rezerwacja', RezerwacjaViewSet, basename='rezerwacja')
router.register('bilet', BiletViewSet, basename='bilet')

urlpatterns = [
    path('', include(router.urls)),
]