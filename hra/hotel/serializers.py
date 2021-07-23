from datetime import date

from django.db.models import Q
from rest_framework import serializers

from hotel.models import Reservation, Room, RoomClass


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

    def validate_rooms(self, rooms):
        if not len(rooms):
            raise serializers.ValidationError(
                'Reservation has to have at least one room')
        return rooms

    def validate(self, data):
        self._validate_dates(data['date_from'], data['date_to'])
        self._validate_rooms_available(
            data['rooms'], data['date_from'], data['date_to'])
        return data

    def _validate_dates(self, date_from, date_to):
        if date_from >= date_to:
            raise serializers.ValidationError(
                'Reservation start date must be before end date')

    def _validate_rooms_available(self, rooms, date_from, date_to):
        """
        Checks if all rooms are available within given time period
        """
        if any(not self._is_available(r, date_from, date_to)
               for r in rooms):
            raise serializers.ValidationError(
                'One of the rooms is not available for reservation within given time')

    def _is_available(
            self,
            room: Room,
            date_from: date,
            date_to: date) -> bool:
        # room is available if both date_from and date_to are before other
        # reservations' start date or after other reservations' end date
        reservations = Reservation.objects.filter(
            (Q(date_from__lt=date_from) | Q(date_from__lt=date_to)) &
            (Q(date_to__gt=date_from) | Q(date_to__gt=date_to)),
            rooms__number=room.number)
        # If any reservation fails above test, room is not available
        return not reservations.count()
