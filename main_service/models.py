from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='plays', blank=True)
    actors = models.ManyToManyField(Actor, related_name='plays', blank=True)

    class Meta:
        verbose_name = "Play"
        verbose_name_plural = "Plays"

    def __str__(self):
        return self.title


class TheaterHall(models.Model):
    name = models.CharField(max_length=255)
    number_of_rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Theater Hall"
        verbose_name_plural = "Theater Halls"

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name='performances')
    theater_hall = models.ForeignKey(TheaterHall, on_delete=models.CASCADE, related_name='performances')
    performance_time = models.DateTimeField()

    class Meta:
        verbose_name = "Performance"
        verbose_name_plural = "Performances"

    def __str__(self):
        return f"{self.play.title} at {self.performance_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"Reservation #{self.id} by {self.user}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('performance', 'row', 'seat')
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"{self.performance} - Row {self.row}, Seat {self.seat}"

    #Metoda do spawdzania czy miejsce jest wolne
    @staticmethod
    def is_seat_taken(performance, row, seat):
        return Ticket.objects.filter(performance=performance, row=row, seat=seat).exists()
    #Metoda do spawdzania czy te miejsce dotycze do sali
    @staticmethod
    def is_valid_seat(performance, row, seat):
        hall = performance.theater_hall
        return (
            1 <= row <= hall.number_of_rows and
            1 <= seat <= hall.seats_per_row
        )
