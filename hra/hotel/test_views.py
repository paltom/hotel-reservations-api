from datetime import date, timedelta
from decimal import Decimal
import unittest

from rest_framework.test import APITestCase
from rest_framework import status
from hotel.exceptions import RoomDeleteError

from hotel.models import Reservation, Room, RoomClass


class RoomViewsTest(APITestCase):
    """
    Test suite for rooms/ endpoint.
    """
    uri = '/rooms/'

    def setUp(self):
        self.room_class = RoomClass.objects.create(
            room_class='T', price=Decimal('30'))
        self.room = Room.objects.create(
            number='123', room_class=self.room_class)
        self.room_uri = self.uri + self.room.number + '/'

    def test_list_rooms(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['number'], self.room.number)
        self.assertEqual(
            response.data[0]['room_class'],
            self.room_class.room_class)

    def test_create_room(self):
        response = self.client.post(
            self.uri, {'number': 'A1', 'room_class': 'T'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)
        self.assertIn(
            'A1', [
                n['number'] for n in list(
                    Room.objects.values('number').iterator())])

    def test_room_detail(self):
        response = self.client.get(self.room_uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], self.room.number)
        self.assertEqual(
            response.data['room_class'],
            self.room_class.room_class)

    def test_update_room(self):
        room_class = RoomClass.objects.create(
            room_class='S', price=Decimal('40'))
        response = self.client.patch(
            self.room_uri, {
                'room_class': room_class.room_class})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.count(), 1)
        self.room.refresh_from_db()
        self.assertEqual(
            self.room.room_class.room_class,
            room_class.room_class)

    def test_delete_room(self):
        response = self.client.delete(self.room_uri)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.count(), 0)

    def test_delete_reserved_room(self):
        Reservation.objects.create(
            date_from=date.today() + timedelta(1),
            date_to=date.today() + timedelta(2),
            name='Smith'
        ).rooms.set([self.room])
        response = self.client.delete(self.room_uri)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            RoomDeleteError.default_detail)


class ReservationViewsTest(APITestCase):
    """
    Test suite for reservations/ endpoint.
    """
    uri = '/reservations/'

    def setUp(self):
        self.room_class = RoomClass.objects.create(
            room_class='T', price=Decimal('30'))
        self.room = Room.objects.create(
            number='123', room_class=self.room_class)
        self.reservation = Reservation.objects.create(
            date_from=date.today(),
            date_to=date.today() + timedelta(3),
            name='Smith'
        )
        self.reservation.rooms.set([self.room])
        self.reservation_uri = self.uri + str(self.reservation.id) + '/'

    def test_list_reservations(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_reservation(self):
        response = self.client.post(self.uri,
                                    {'rooms': ['123'],
                                     'date_from': date.today() + timedelta(7),
                                     'date_to': date.today() + timedelta(9),
                                     'name': 'Smith'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_reservation_detail(self):
        response = self.client.get(self.reservation_uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.reservation.name)
        self.assertEqual(
            response.data['rooms'],
            [self.room.number])
        self.assertEqual(
            response.data['duration'],
            (self.reservation.date_to -
             self.reservation.date_from).days)
        self.assertEqual(response.data['total_cost'], 90)

    def test_update_reservation(self):
        response = self.client.patch(
            self.reservation_uri, {
                'date_from': date.today(),
                'date_to': date.today() + timedelta(1)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.count(), 1)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.duration, 1)

    def test_delete_reservation(self):
        response = self.client.delete(self.reservation_uri)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)
