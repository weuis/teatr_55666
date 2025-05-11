from rest_framework import serializers
from main_service.models import (
    Genre, Actor, Play, TheaterHall,
    Performance, Reservation, Ticket
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class PlaySerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    actors = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True)

    class Meta:
        model = Play
        fields = '__all__'


class PlayDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = '__all__'


class TheaterHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterHall
        fields = '__all__'


class PerformanceSerializer(serializers.ModelSerializer):
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())
    theater_hall = serializers.PrimaryKeyRelatedField(queryset=TheaterHall.objects.all())

    class Meta:
        model = Performance
        fields = '__all__'


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True)
    theater_hall = TheaterHallSerializer(read_only=True)
    taken_seats = serializers.SerializerMethodField()
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = '__all__'

    #Zwraca dla uzytkownika informacje(liste) miejsc ktore są zajęte
    def get_taken_seats(self, obj):
        return [
            {"row": ticket.row, "seat": ticket.seat}
            for ticket in obj.tickets.all()
        ]

    # Zwraca dla uzytkownika informacje(liste) miejsc ktore są wolne
    def get_available_seats(self, obj):
        taken_seats = set(
            (ticket.row, ticket.seat) for ticket in obj.tickets.all()
        )
        available_seats = [
            {"row": row, "seat": seat}
            for row in range(1, obj.theater_hall.number_of_rows + 1)
            for seat in range(1, obj.theater_hall.seats_per_row + 1)
            if (row, seat) not in taken_seats
        ]
        return available_seats

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def validate(self, attrs):
        row = attrs.get('row')
        seat = attrs.get('seat')
        performance = attrs.get('performance')


        # Sprawdzamy czy te miejsce dotycze do sali z konkretnym wydarzeniem
        if not Ticket.is_valid_seat(performance, row, seat):
            raise serializers.ValidationError(
                f"Seat (row {row}, seat {seat}) is not valid"
            )
        #Spawdzamy czy miejsce jest wolne na wydarzenie
        if self.instance is None:
            if Ticket.is_seat_taken(performance, row, seat):
                raise serializers.ValidationError(
                    f"Seat (row {row}, seat {seat}) is already taken for this performance."
                )

        return attrs


class TicketDetailSerializer(serializers.ModelSerializer):
    performance = PerformanceDetailSerializer(read_only=True)
    reservation = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
