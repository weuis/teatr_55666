from rest_framework import serializers
from .models import (
    Gatunek, Aktor, Sztuka, SalaTeatralna,
    Przedstawienie, Rezerwacja, Bilet
)


class GatunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gatunek
        fields = '__all__'


class AktorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktor
        fields = '__all__'


class SztukaSerializer(serializers.ModelSerializer):
    gatunki = serializers.PrimaryKeyRelatedField(queryset=Gatunek.objects.all(), many=True)
    aktorzy = serializers.PrimaryKeyRelatedField(queryset=Aktor.objects.all(), many=True)

    class Meta:
        model = Sztuka
        fields = '__all__'


class SztukaDetailSerializer(serializers.ModelSerializer):
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
    sztuka = serializers.PrimaryKeyRelatedField(queryset=Sztuka.objects.all())
    sala_teatralna = serializers.PrimaryKeyRelatedField(queryset=SalaTeatralna.objects.all())

    class Meta:
        model = Przedstawienie
        fields = '__all__'


class PrzedstawienieDetailSerializer(serializers.ModelSerializer):
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


class BiletDetailSerializer(serializers.ModelSerializer):
    przedstawienie = PrzedstawienieDetailSerializer(read_only=True)
    rezerwacja = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bilet
        fields = '__all__'

