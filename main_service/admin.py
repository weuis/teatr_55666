from django.contrib import admin
from main_service.models import (
    Genre,
    Actor,
    Play,
    TheaterHall,
    Performance,
    Reservation,
    Ticket
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title", "description")
    filter_horizontal = ("genres", "actors")


@admin.register(TheaterHall)
class TheaterHallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "number_of_rows", "seats_per_row")
    search_fields = ("name",)
    list_filter = ("number_of_rows",)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "play", "theater_hall", "performance_time")
    list_filter = ("theater_hall", "performance_time")
    search_fields = ("play__title",)
    autocomplete_fields = ("play", "theater_hall")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    date_hierarchy = "created_at"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "performance", "reservation", "row", "seat")
    list_filter = ("performance", "row")
    search_fields = ("reservation__user__username",)
    autocomplete_fields = ("performance", "reservation")
