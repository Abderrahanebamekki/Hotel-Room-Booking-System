# Generated by Django 5.0.2 on 2024-03-20 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_remove_amenityhotel_amenity1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='location',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
