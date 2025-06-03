from rest_framework import serializers

class TicketmasterEventSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()
    dates = serializers.JSONField()
    images = serializers.ListField()
    _embedded = serializers.JSONField()
