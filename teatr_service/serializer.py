from rest_framework import serializers
from teatr_service.models import Gatunek, Aktor, Sztuka, SalaTeatralna, Przedstawienie, Rezerwacja, Bilet

class GatunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gatunek
        fields = '__all__'

class AktorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktor
        fields = '__all__'

class SztukaSerializer(serializers.ModelSerializer):
    gatunki = GatunekSerializer(many=True, read_only=True)
    aktorzy = AktorSerializer(many=True, read_only=True)

    class Meta:
        model = Sztuka
        fields = '__all__'

class SalaTeatralnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaTeatralna
        fields = '__all__'

class PrzedstawienieSerializer(serializers.ModelSerializer):
    sztuka = SztukaSerializer(read_only=True)
    sala_teatralna = SalaTeatralnaSerializer(read_only=True)

    class Meta:
        model = Przedstawienie
        fields = '__all__'

class RezerwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rezerwacja
        fields = '__all__'

class BiletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilet
        fields = '__all__'
