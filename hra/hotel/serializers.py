from rest_framework import serializers
from hotel.models import Room, RoomClass, Reservation


class RoomClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomClass
        fields = ['room_class', 'price']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'room_class']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'date_from',
            'date_to',
            'name',
            'rooms',
            'total_cost',
            'duration']
