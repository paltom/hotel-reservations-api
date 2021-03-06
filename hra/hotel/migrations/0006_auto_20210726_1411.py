# Generated by Django 3.2.5 on 2021-07-26 14:11
from decimal import Decimal

from django.db import migrations


def create_room_classes(apps, schema_editor):
    RoomClass = apps.get_model('hotel', 'RoomClass')
    RoomClass.objects.create(room_class='A', price=Decimal('200'))
    RoomClass.objects.create(room_class='B', price=Decimal('150'))
    RoomClass.objects.create(room_class='C', price=Decimal('100'))
    RoomClass.objects.create(room_class='D', price=Decimal('50'))


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_auto_20210724_1618'),
    ]

    operations = [
        migrations.RunPython(create_room_classes)
    ]
