from django.contrib import admin
from teatr_service.models import (
    Gatunek,
    Aktor,
    Sztuka,
    SalaTeatralna,
    Przedstawienie,
    Rezerwacja,
    Bilet
)

admin.site.register(Gatunek)
admin.site.register(Aktor)
admin.site.register(Sztuka)
admin.site.register(SalaTeatralna)
admin.site.register(Przedstawienie)
admin.site.register(Rezerwacja)
admin.site.register(Bilet)

