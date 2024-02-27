# Generated by Django 5.0.2 on 2024-02-25 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
