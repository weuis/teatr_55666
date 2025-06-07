from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny

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
from main_service.permissions import IsAdminOrReadOnly, IsAuthenticatedForWriteOnly


@extend_schema(tags=["Genres"])
class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing genres.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["Actors"])
class ActorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing actors.
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    search_fields = ['first_name', 'last_name']
    permission_classes = [AllowAny]


    @extend_schema(
        parameters=[
            OpenApiParameter("search", str, OpenApiParameter.QUERY, description="Search by actor's first or last name"),
        ],
        description="List all actors with optional search."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Plays"])
class PlayViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing plays.
    """
    search_fields = ['title', 'description']
    ordering_fields = ['title']
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Play.objects.prefetch_related('genres', 'actors')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PlayDetailSerializer
        return PlaySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("search", str, OpenApiParameter.QUERY, description="Search by play title or description"),
            OpenApiParameter("ordering", str, OpenApiParameter.QUERY, description="Order by title (e.g., ?ordering=title or ?ordering=-title)"),
        ],
        description="List all plays with optional search and ordering."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Theater Halls"])
class TheaterHallViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing theater halls.
    """
    queryset = TheaterHall.objects.all()
    serializer_class = TheaterHallSerializer
    search_fields = ['name']
    ordering_fields = ['number_of_rows', 'seats_per_row']
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter("search", str, OpenApiParameter.QUERY, description="Search by theater hall name"),
            OpenApiParameter("ordering", str, OpenApiParameter.QUERY, description="Order by number_of_rows or seats_per_row"),
        ],
        description="List all theater halls with optional search and ordering."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Performances"])
class PerformanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing performanc.css.
    """
    search_fields = ['play__title']
    ordering_fields = ['performance_time']
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Performance.objects.select_related('play', 'theater_hall')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PerformanceDetailSerializer
        return PerformanceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("search", str, OpenApiParameter.QUERY, description="Search by play title"),
            OpenApiParameter("ordering", str, OpenApiParameter.QUERY, description="Order by performance_time"),
        ],
        description="List all performanc.css with optional search and ordering."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Reservations"])
class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reservations.
    Only authenticated users can create or list their reservations.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticatedForWriteOnly]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Reservation.objects.filter(user=user)
        return Reservation.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        description="List authenticated user's reservations."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Tickets"])
class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tickets.
    """
    ordering_fields = ['row', 'seat']
    permission_classes = [IsAuthenticatedForWriteOnly]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Ticket.objects.select_related('performance', 'reservation')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TicketDetailSerializer
        return TicketSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("ordering", str, OpenApiParameter.QUERY, description="Order by row or seat"),
        ],
        description="List tickets with optional ordering."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
