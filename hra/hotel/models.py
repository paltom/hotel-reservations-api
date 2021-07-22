from decimal import Decimal
from django.core.validators import DecimalValidator, MinValueValidator, RegexValidator
from django.db import models


class RoomClass(models.Model):
    room_class = models.CharField(
        'class of the room', primary_key=True, max_length=3, validators=[RegexValidator('[A-Z]')])
    price = models.DecimalField("room's class' price for one day", decimal_places=2,
                                max_digits=7, validators=[MinValueValidator(Decimal('0.00'))])


class Room(models.Model):
    number = models.CharField('room number', primary_key=True, max_length=5)
    room_class = models.ForeignKey(
        RoomClass, on_delete=models.DO_NOTHING, related_name='+')
