# Generated by Django 5.0.2 on 2024-03-20 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_alter_hotel_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomtype',
            name='price',
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
