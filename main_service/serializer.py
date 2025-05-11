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

    class Meta:
        model = Performance
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketDetailSerializer(serializers.ModelSerializer):
    performance = PerformanceDetailSerializer(read_only=True)
    reservation = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
