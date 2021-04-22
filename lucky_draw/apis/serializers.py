from rest_framework import serializers
from .models import User, Ticket, Event


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model."""
    class Meta:
        model = User
        fields = ['username', 'email']


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket Model."""
    class Meta:
        model = Ticket
        fields = ['id', 'status']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event Model."""
    class Meta:
        model = Event
        fields = '__all__'


class FutureEventSerializer(serializers.ModelSerializer):
    """Serializer for Event Model for future Events."""
    class Meta:
        model = Event
        fields = ['title', 'date_time', 'prize']
