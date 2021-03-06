# Generated by Django 3.2.5 on 2021-07-23 07:09

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomClass',
            fields=[
                ('room_class', models.CharField(max_length=1, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('[A-Z]')], verbose_name='class of the room')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name="room's class' price for one day")),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='room number')),
                ('room_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms+', to='hotel.roomclass')),
            ],
        ),
    ]
