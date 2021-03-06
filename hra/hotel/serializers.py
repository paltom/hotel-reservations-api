from datetime import date

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
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
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.CharField(required=False, max_length=100)

    class Meta:
        model = Reservation
        fields = [
            'id',
            'date_from',
            'date_to',
            'name',
            'rooms',
            'total_cost',
            'duration',
            'owner']
        read_only_fields = ['id']

    def validate_date_from(self, value: date):
        if value < date.today():
            raise serializers.ValidationError(
                'Reservation cannot start in the past')
        return value

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
        Checks if all rooms are available within given time period.
        """
        if any(not self._is_available(r, date_from, date_to)
               for r in rooms):
            raise serializers.ValidationError(
                'Selected rooms are not available for reservation within given time. '
                'Try different rooms or different reservation time.')

    def _is_available(
            self,
            room: Room,
            date_from: date,
            date_to: date) -> bool:
        # room is available if both date_from and date_to are before other
        # reservations' start date or after other reservations' end date
        reservation_collisions = Reservation.objects.filter(
            (Q(date_from__lt=date_from) | Q(date_from__lt=date_to)) &
            (Q(date_to__gt=date_from) | Q(date_to__gt=date_to)),
            rooms__number=room.number)
        if self.instance is not None:
            # Updating existing reservation, so remove it from collisions
            reservation_collisions = reservation_collisions.exclude(
                pk=self.instance.id)
        # If any reservation passes above test, room is not available
        return not reservation_collisions.count()


class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'reservations',
            'first_name',
            'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
