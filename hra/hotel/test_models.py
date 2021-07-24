import unittest
from datetime import date, timedelta
from decimal import Decimal

from django.db.utils import IntegrityError
from django.test import TestCase

from hotel.models import Reservation, Room, RoomClass


class RoomClassTest(TestCase):
    """
    Test suite for RoomClass model.
    """

    def test_room_class(self):
        RoomClass.objects.create(room_class='T', price=Decimal('50'))
        room_class = RoomClass.objects.get(pk='T')
        self.assertEqual(room_class.room_class, 'T')
        self.assertEqual(room_class.price, 50.0)

    def test_room_class_requires_price(self):
        with self.assertRaises(IntegrityError):
            RoomClass.objects.create(room_class='T')

    @unittest.expectedFailure
    def test_room_class_requires_room_class(self):
        # django will insert blank string as room_class field (primary key)
        # blank=False on models is used during validation in
        # serializers, not by DB
        with self.assertRaises(IntegrityError):
            RoomClass.objects.create(price=50)


class RoomTest(TestCase):
    """
    Test suite for Room model.
    """

    def setUp(self):
        self.room_class_t = RoomClass.objects.create(
            room_class='T', price=Decimal('50'))

    def test_room(self):
        Room.objects.create(number='A123', room_class=self.room_class_t)
        room = Room.objects.get(pk='A123')
        self.assertEqual(room.room_class.room_class, 'T')
        self.assertEqual(room.room_class.price, 50)
        self.assertEqual(room.number, 'A123')
        self.assertEqual(room.reservations.count(), 0)

    def room_numbers_are_unique(self):
        Room.objects.create(number='A123', room_class=self.room_class_t)
        with self.assertRaises(IntegrityError):
            room_class_s = RoomClass.objects.create(
                room_class='S', price=Decimal('50'))
            Room.objects.create(number='A123', room_class=room_class_s)

    def test_room_without_class(self):
        with self.assertRaises(IntegrityError):
            Room.objects.create(number='A123')

    @unittest.expectedFailure
    def test_room_without_number(self):
        # same issue as with empty room_class - primary key as CharField gets
        # created with empty room number as default - validations are run in
        # serializers
        with self.assertRaises(IntegrityError):
            Room.objects.create(room_class=self.room_class_t)

    def test_rooms_are_deleted_when_room_class_is_deleted(self):
        Room.objects.create(number='A123', room_class=self.room_class_t)
        Room.objects.create(number='B456', room_class=self.room_class_t)
        self.room_class_t.delete()
        self.assertEqual(Room.objects.count(), 0)


class ReservationTest(TestCase):
    """
    Test suite for Reservation model.
    """

    def setUp(self):
        self.room_class_t = RoomClass.objects.create(
            room_class='T', price=Decimal('50'))
        self.room_class_s = RoomClass.objects.create(
            room_class='S', price=Decimal('75'))
        self.room_t = Room.objects.create(
            room_class=self.room_class_t, number='1T')
        self.room_s = Room.objects.create(
            room_class=self.room_class_s, number='1S')

    def test_reservation(self):
        Reservation.objects.create(
            name='Smith',
            date_from=date.today(),
            date_to=date.today() + timedelta(1),
        ).rooms.set([self.room_s, self.room_t])
        reservation = Reservation.objects.get(pk=1)
        self.assertEqual(reservation.name, 'Smith')
        self.assertEqual(reservation.date_from, date.today())
        self.assertEqual(reservation.date_to, date.today() + timedelta(1))
        self.assertEqual(reservation.total_cost, 125)
        self.assertEqual(reservation.duration, 1)

    @unittest.expectedFailure
    def test_reservation_without_rooms(self):
        # from documentation:
        # null has no effect since there is no way to require a relationship at
        # the database level.
        # creating reservation without rooms is possible on the DB level
        # validations are performed on serializers
        with self.assertRaises(IntegrityError):
            Reservation.objects.create(
                name='Smith',
                date_from=date.today(),
                date_to=date.today() + timedelta(1),
            )

    @unittest.expectedFailure
    def test_reservation_is_removed_if_rooms_are_removed(self):
        # same as creating reservation without rooms - cannot be enforced on
        # the DB level
        Reservation.objects.create(
            name='Smith',
            date_from=date.today(),
            date_to=date.today() + timedelta(1),
        ).rooms.set([self.room_s, self.room_t])
        self.room_s.delete()
        self.assertEqual(Reservation.objects.count(), 0)
