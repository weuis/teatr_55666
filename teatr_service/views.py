from rest_framework import viewsets, filters
from teatr_service.models import (
    Gatunek, Aktor, Sztuka, SalaTeatralna,
    Przedstawienie, Rezerwacja, Bilet
)
from teatr_service.serializer import (
    GatunekSerializer, AktorSerializer, SztukaSerializer,
    SalaTeatralnaSerializer, PrzedstawienieSerializer,
    RezerwacjaSerializer, BiletSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class GatunekViewSet(viewsets.ModelViewSet):
    queryset = Gatunek.objects.all()
    serializer_class = GatunekSerializer


class AktorViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Aktor.objects.all()

    def get_serializer_class(self):
        return AktorSerializer

    search_fields = ['imie', 'nazwisko']
    ordering_fields = ['nazwisko', 'imie']


class SztukaViewSet(viewsets.ModelViewSet):
    serializer_class = SztukaSerializer
    search_fields = ['tytul', 'opis']
    ordering_fields = ['tytul']

    def get_queryset(self):
        return Sztuka.objects.prefetch_related('gatunki', 'aktorzy')


class SalaTeatralnaViewSet(viewsets.ModelViewSet):
    queryset = SalaTeatralna.objects.all()
    serializer_class = SalaTeatralnaSerializer
    search_fields = ['nazwa']
    ordering_fields = ['liczba_rzedow', 'miejsca_w_rzedzie']


class PrzedstawienieViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Przedstawienie.objects.select_related('sztuka', 'sala_teatralna')

    def get_serializer_class(self):
        return PrzedstawienieSerializer

    search_fields = ['sztuka__tytul']
    ordering_fields = ['czas_wystepu']


class RezerwacjaViewSet(viewsets.ModelViewSet):
    serializer_class = RezerwacjaSerializer
    def get_queryset(self):
        return Rezerwacja.objects.filter(uzytkownik=self.request.user)


class BiletViewSet(viewsets.ModelViewSet):
    queryset = Bilet.objects.all()
    serializer_class = BiletSerializer
    ordering_fields = ['rzad', 'miejsce']
