from django.db import models
from django.conf import settings

class Gatunek(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class Aktor(models.Model):
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Sztuka(models.Model):
    tytul = models.CharField(max_length=255)
    opis = models.TextField()
    gatunki = models.ManyToManyField(Gatunek, related_name='sztuki', blank=True)
    aktorzy = models.ManyToManyField(Aktor, related_name='sztuki', blank=True)

    def __str__(self):
        return self.tytul


class SalaTeatralna(models.Model):
    nazwa = models.CharField(max_length=255)
    liczba_rzedow = models.PositiveIntegerField()
    miejsca_w_rzedzie = models.PositiveIntegerField()

    def __str__(self):
        return self.nazwa


class Przedstawienie(models.Model):
    sztuka = models.ForeignKey(Sztuka, on_delete=models.CASCADE, related_name='przedstawienia')
    sala_teatralna = models.ForeignKey(SalaTeatralna, on_delete=models.CASCADE, related_name='przedstawienia')
    czas_wystepu = models.DateTimeField()

    def __str__(self):
        return f"{self.sztuka.tytul} o {self.czas_wystepu}"


class Rezerwacja(models.Model):
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    uzytkownik = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rezerwacje"
    )

    def __str__(self):
        return f"Rezerwacja #{self.id} przez {self.uzytkownik}"


class Bilet(models.Model):
    rzad = models.PositiveIntegerField()
    miejsce = models.PositiveIntegerField()
    przedstawienie = models.ForeignKey(Przedstawienie, on_delete=models.CASCADE, related_name='bilety')
    rezerwacja = models.ForeignKey(Rezerwacja, on_delete=models.CASCADE, related_name='bilety')

    class Meta:
        unique_together = ('przedstawienie', 'rzad', 'miejsce')
