# Generated by Django 5.0.2 on 2024-03-26 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0008_room_hotel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bed_room',
            unique_together={('bed', 'room')},
        ),
    ]
