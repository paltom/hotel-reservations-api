from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.models import User

from django.test import TestCase

from hotel.models import Reservation, Room, RoomClass
from hotel.serializers import (ReservationSerializer, RoomClassSerializer,
                               RoomSerializer)


class RoomClassSerializerTest(TestCase):
    """
    Test suite for RoomClass serialization.
    """

    def setUp(self):
        self.room_class_valid_attributes = {
            'room_class': 'T',
            'price': Decimal('125')
        }
        self.room_class_deserializer_valid_data = {
            'room_class': 'S',
            'price': '99.99'
        }
        self.room_class = RoomClass.objects.create(
            **self.room_class_valid_attributes)
        self.serializer = RoomClassSerializer(self.room_class)
        self.deserializer = RoomClassSerializer(
            data=self.room_class_deserializer_valid_data)

    def test_serializer_contains_all_fields(self):
        self.assertCountEqual(
            self.serializer.data.keys(), [
                'room_class', 'price'])

    def test_data_is_correctly_serialized(self):
        self.assertEqual(
            self.serializer.data['room_class'],
            self.room_class_valid_attributes['room_class'])
        self.assertEqual(
            self.serializer.data['price'],
            '{:5.2f}'.format(self.room_class_valid_attributes['price']))

    def test_deserializer_creates_valid_instance(self):
        self.assertTrue(self.deserializer.is_valid())
        room_class = self.deserializer.save()
        self.assertEqual(room_class.room_class,
                         self.room_class_deserializer_valid_data['room_class'])
        self.assertEqual(
            room_class.price, Decimal(
                self.room_class_deserializer_valid_data['price']))

    def _test_invalid_fields_deserialization(self, **kwargs):
        # requires Python 3.9
        data = self.room_class_deserializer_valid_data | kwargs
        deserializer = RoomClassSerializer(data=data)
        self.assertFalse(deserializer.is_valid())
        self.assertCountEqual(deserializer.errors, kwargs.keys())

    def test_price_cannot_be_negative(self):
        self._test_invalid_fields_deserialization(price='-0.01')

    def test_price_cannot_be_too_large(self):
        self._test_invalid_fields_deserialization(price='100000')

    def test_room_class_cannot_be_empty(self):
        self._test_invalid_fields_deserialization(room_class='')

    def test_room_class_wrong_format(self):
        self._test_invalid_fields_deserialization(room_class='t')
        self._test_invalid_fields_deserialization(room_class='AB')


class RoomSerializerTest(TestCase):
    """
    Test suite for Room serialization.
    """

    def setUp(self):
        self.room_valid_attributes = {
            'room_class': 'T',
            'number': 'A123'
        }
        self.room_deserializer_valid_data = self.room_valid_attributes | {
            'number': 'B456'
        }
        self.room_class = RoomClass.objects.create(
            room_class=self.room_valid_attributes['room_class'], price=Decimal('10'))
        self.room = Room.objects.create(
            **(self.room_valid_attributes | {
                'room_class': self.room_class}))
        self.serializer = RoomSerializer(self.room)
        self.deserializer = RoomSerializer(
            data=self.room_deserializer_valid_data)

    def test_serializer_contains_all_fields(self):
        self.assertCountEqual(
            self.serializer.data.keys(), [
                'room_class', 'number'])

    def test_data_is_correctly_serialized(self):
        self.assertEqual(
            self.serializer.data['room_class'],
            self.room_valid_attributes['room_class'])
        self.assertEqual(
            self.serializer.data['number'],
            self.room_valid_attributes['number'])

    def test_deserializer_creates_valid_instance(self):
        self.assertTrue(self.deserializer.is_valid())
        room = self.deserializer.save()
        self.assertEqual(room.room_class.room_class,
                         self.room_deserializer_valid_data['room_class'])
        self.assertEqual(
            room.number, self.room_deserializer_valid_data['number'])

    def _test_invalid_fields_deserialization(self, **kwargs):
        # requires Python 3.9
        data = self.room_deserializer_valid_data | kwargs
        deserializer = RoomSerializer(data=data)
        self.assertFalse(deserializer.is_valid())
        self.assertCountEqual(deserializer.errors, kwargs.keys())

    def test_number_cannot_be_empty(self):
        self._test_invalid_fields_deserialization(number='')

    def test_number_cannot_be_too_long(self):
        self._test_invalid_fields_deserialization(number='123456')

    def test_cannot_create_room_when_room_class_not_exist(self):
        self._test_invalid_fields_deserialization(room_class='N')


class ReservationSerializerTest(TestCase):
    """
    Test suite for Reservation serialization.
    """

    def setUp(self):
        self.owner = User.objects.create(username='test', last_name='Brown')
        self.reservation_valid_attributes = {
            'date_from': (date.today() + timedelta(7)).isoformat(),
            'date_to': (date.today() + timedelta(8)).isoformat(),
            'duration': 1,
            'name': 'Brown',
            'rooms': ['T1'],
            'total_cost': 10,
            'id': 1,
            'owner': self.owner.username
        }
        self.reservation_deserializer_valid_data = {
            'date_from': date.today().isoformat(),
            'date_to': (date.today() + timedelta(3)).isoformat(),
            'name': 'Smith',
            'rooms': ['T1', 'S2']
        }
        self.room_class_t = RoomClass.objects.create(
            room_class='T', price=Decimal(
                self.reservation_valid_attributes['total_cost']))
        self.room_class_s = RoomClass.objects.create(
            room_class='S', price=Decimal('20'))
        self.room_t = Room.objects.create(
            **{'number': self.reservation_valid_attributes['rooms'][0],
               'room_class': self.room_class_t})
        self.room_s = Room.objects.create(
            **{'number': self.reservation_deserializer_valid_data['rooms'][1],
               'room_class': self.room_class_s})
        self.reservation = Reservation.objects.create(
            date_from=date.fromisoformat(
                self.reservation_valid_attributes['date_from']),
            date_to=date.fromisoformat(
                self.reservation_valid_attributes['date_to']),
            name=self.reservation_valid_attributes['name'],
            owner=self.owner)
        self.reservation.rooms.set([self.room_t])
        self.serializer = ReservationSerializer(self.reservation)
        self.deserializer = ReservationSerializer(
            data=self.reservation_deserializer_valid_data)

    def test_serializer_contains_all_fields(self):
        self.assertCountEqual(
            self.serializer.data.keys(),
            self.reservation_valid_attributes.keys())

    def test_data_is_correctly_serialized(self):
        for attr in self.reservation_valid_attributes.keys():
            self.assertEqual(
                self.serializer.data[attr],
                self.reservation_valid_attributes[attr])

    def test_deserializer_creates_valid_instance(self):
        self.assertTrue(self.deserializer.is_valid())
        reservation = self.deserializer.save(owner=self.owner)
        self.assertEqual(reservation.date_from.isoformat(),
                         self.reservation_deserializer_valid_data['date_from'])
        self.assertEqual(reservation.date_to.isoformat(),
                         self.reservation_deserializer_valid_data['date_to'])
        self.assertEqual(reservation.name,
                         self.reservation_deserializer_valid_data['name'])
        self.assertCountEqual(reservation.rooms.all(),
                              [self.room_t, self.room_s])

    def _test_invalid_fields_deserialization(self, error_key=None, **kwargs):
        # requires Python 3.9
        data = self.reservation_deserializer_valid_data | kwargs
        deserializer = ReservationSerializer(data=data)
        self.assertFalse(deserializer.is_valid())
        self.assertCountEqual(
            deserializer.errors,
            [error_key] if error_key is not None else kwargs.keys())

    def test_start_date_after_or_equal_to_end_date(self):
        self._test_invalid_fields_deserialization(
            'non_field_errors',
            date_from=date.today().isoformat(),
            date_to=date.today().isoformat())
        self._test_invalid_fields_deserialization(
            'non_field_errors',
            date_from=(date.today() + timedelta(2)).isoformat(),
            date_to=date.today().isoformat())

    def test_rooms_empty(self):
        self._test_invalid_fields_deserialization(rooms=[])

    def test_room_number_does_not_exist(self):
        self._test_invalid_fields_deserialization(rooms=['A1'])

    def test_room_is_not_available_for_reservation(self):
        self._test_invalid_fields_deserialization(
            'non_field_errors', rooms=[
                self.reservation.rooms.all()[0].number],
            date_from=self.reservation.date_from - timedelta(1),
            date_to=self.reservation.date_to + timedelta(1))

    def test_start_date_in_the_past(self):
        self._test_invalid_fields_deserialization(
            date_from=date.today() - timedelta(1))
