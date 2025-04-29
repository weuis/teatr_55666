from django.contrib import admin
from .models import (
    Gatunek,
    Aktor,
    Sztuka,
    SalaTeatralna,
    Przedstawienie,
    Rezerwacja,
    Bilet
)


@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    list_display = ("id", "nazwa")
    search_fields = ("nazwa",)


@admin.register(Aktor)
class AktorAdmin(admin.ModelAdmin):
    list_display = ("id", "imie", "nazwisko")
    search_fields = ("imie", "nazwisko")


@admin.register(Sztuka)
class SztukaAdmin(admin.ModelAdmin):
    list_display = ("id", "tytul")
    search_fields = ("tytul", "opis")
    filter_horizontal = ("gatunki", "aktorzy")


@admin.register(SalaTeatralna)
class SalaTeatralnaAdmin(admin.ModelAdmin):
    list_display = ("id", "nazwa", "liczba_rzedow", "miejsca_w_rzedzie")
    search_fields = ("nazwa",)
    list_filter = ("liczba_rzedow",)


@admin.register(Przedstawienie)
class PrzedstawienieAdmin(admin.ModelAdmin):
    list_display = ("id", "sztuka", "sala_teatralna", "czas_wystepu")
    list_filter = ("sala_teatralna", "czas_wystepu")
    search_fields = ("sztuka__tytul",)
    autocomplete_fields = ("sztuka", "sala_teatralna")


@admin.register(Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    list_display = ("id", "uzytkownik", "data_utworzenia")
    list_filter = ("data_utworzenia",)
    search_fields = ("uzytkownik__username",)
    date_hierarchy = "data_utworzenia"


@admin.register(Bilet)
class BiletAdmin(admin.ModelAdmin):
    list_display = ("id", "przedstawienie", "rezerwacja", "rzad", "miejsce")
    list_filter = ("przedstawienie", "rzad")
    search_fields = ("rezerwacja__uzytkownik__username",)
    autocomplete_fields = ("przedstawienie", "rezerwacja")
