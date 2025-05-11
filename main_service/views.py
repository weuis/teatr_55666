from rest_framework import viewsets
from main_service.models import (
    Genre, Actor, Play, TheaterHall,
    Performance, Reservation, Ticket
)
from main_service.serializer import (
    GenreSerializer, ActorSerializer, PlaySerializer, PlayDetailSerializer,
    TheaterHallSerializer,
    PerformanceSerializer, PerformanceDetailSerializer,
    ReservationSerializer,
    TicketSerializer, TicketDetailSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['last_name', 'first_name']


class PlayViewSet(viewsets.ModelViewSet):
    search_fields = ['title', 'description']
    ordering_fields = ['title']

    def get_queryset(self):
        return Play.objects.prefetch_related('genres', 'actors')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PlayDetailSerializer
        return PlaySerializer


class TheaterHallViewSet(viewsets.ModelViewSet):
    queryset = TheaterHall.objects.all()
    serializer_class = TheaterHallSerializer
    search_fields = ['name']
    ordering_fields = ['number_of_rows', 'seats_per_row']


class PerformanceViewSet(viewsets.ModelViewSet):
    search_fields = ['play__title']
    ordering_fields = ['performance_time']

    def get_queryset(self):
        return Performance.objects.select_related('play', 'theater_hall')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PerformanceDetailSerializer
        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    ordering_fields = ['row', 'seat']

    def get_queryset(self):
        return Ticket.objects.select_related('performance', 'reservation')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TicketDetailSerializer
        return TicketSerializer
