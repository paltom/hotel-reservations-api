from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class RoomClass(models.Model):
    room_class = models.CharField(
        'class of the room',
        primary_key=True,
        max_length=1,
        validators=[
            RegexValidator('[A-Z]')])
    price = models.DecimalField(
        "room's class' price for one day",
        decimal_places=2,
        max_digits=7,
        validators=[
            MinValueValidator(
                Decimal('0.00'))])


class Reservation(models.Model):
    date_from = models.DateField('start date of reservation')
    date_to = models.DateField('end date of reservation')
    name = models.CharField(
        'name of the person who made reservation', max_length=100)

    @property
    def total_cost(self):
        return sum([r.room_class.price for r in self.rooms.iterator()])

    @property
    def duration(self):
        return self.date_to - self.date_from


class Room(models.Model):
    number = models.CharField('room number', primary_key=True, max_length=5)
    room_class = models.ForeignKey(
        RoomClass, on_delete=models.CASCADE, related_name='rooms+')
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        related_name='rooms',
        null=True,
        blank=True,
        default=None)
