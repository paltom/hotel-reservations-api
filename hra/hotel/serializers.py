from rest_framework import serializers
from hotel.models import Room, RoomClass


class RoomClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomClass
        fields = ['room_class', 'price']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'room_class']
