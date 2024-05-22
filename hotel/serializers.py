from rest_framework import serializers
from .models import Hotel, Room


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'location', 'ville', 'email', 'phone_num', 'description', 'nb_star']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['price', 'nb_bed', 'room_type']