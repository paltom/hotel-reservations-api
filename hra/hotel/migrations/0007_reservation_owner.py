# Generated by Django 3.2.5 on 2021-07-27 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0006_auto_20210726_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='auth.user'),
            preserve_default=False,
        ),
    ]
