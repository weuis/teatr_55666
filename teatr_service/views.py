from rest_framework import viewsets
from teatr_service.models import (
    Gatunek, Aktor, Sztuka, SalaTeatralna,
    Przedstawienie, Rezerwacja, Bilet
)
from teatr_service.serializer import (
    GatunekSerializer, AktorSerializer, SztukaSerializer, SztukaDetailSerializer,
    SalaTeatralnaSerializer,
    PrzedstawienieSerializer, PrzedstawienieDetailSerializer,
    RezerwacjaSerializer,
    BiletSerializer, BiletDetailSerializer
)


class GatunekViewSet(viewsets.ModelViewSet):
    queryset = Gatunek.objects.all()
    serializer_class = GatunekSerializer


class AktorViewSet(viewsets.ModelViewSet):
    queryset = Aktor.objects.all()
    serializer_class = AktorSerializer
    search_fields = ['imie', 'nazwisko']
    ordering_fields = ['nazwisko', 'imie']


class SztukaViewSet(viewsets.ModelViewSet):
    search_fields = ['tytul', 'opis']
    ordering_fields = ['tytul']

    def get_queryset(self):
        return Sztuka.objects.prefetch_related('gatunki', 'aktorzy')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SztukaDetailSerializer
        return SztukaSerializer


class SalaTeatralnaViewSet(viewsets.ModelViewSet):
    queryset = SalaTeatralna.objects.all()
    serializer_class = SalaTeatralnaSerializer
    search_fields = ['nazwa']
    ordering_fields = ['liczba_rzedow', 'miejsca_w_rzedzie']


class PrzedstawienieViewSet(viewsets.ModelViewSet):
    search_fields = ['sztuka__tytul']
    ordering_fields = ['czas_wystepu']

    def get_queryset(self):
        return Przedstawienie.objects.select_related('sztuka', 'sala_teatralna')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PrzedstawienieDetailSerializer
        return PrzedstawienieSerializer


class RezerwacjaViewSet(viewsets.ModelViewSet):
    serializer_class = RezerwacjaSerializer

    def get_queryset(self):
        return Rezerwacja.objects.filter(uzytkownik=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uzytkownik=self.request.user)


class BiletViewSet(viewsets.ModelViewSet):
    ordering_fields = ['rzad', 'miejsce']

    def get_queryset(self):
        return Bilet.objects.select_related('przedstawienie', 'rezerwacja')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BiletDetailSerializer
        return BiletSerializer
