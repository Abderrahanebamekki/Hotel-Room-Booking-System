from _datetime import datetime
from hotel.models import Hotel, Room
from hotel.serializer import HotelSerializer

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import connection
from .models import Hotel
from .serializers import HotelSerializer, RoomSerializer


class Search(APIView):
    def get(self, request):
        destination = request.query_params.get('destination')
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')
        amenities = request.query_params.get('amenities')
        max_price = request.query_params.get('max_price')
        min_price = request.query_params.get('min_price')
        nb_star = request.query_params.get('nb_star')

        try:
            checkin = datetime.strptime(checkin, "%Y-%m-%d")
            checkout = datetime.strptime(checkout, "%Y-%m-%d")
            # if max_price is not None:
            #     max_price = float(max_price)
            # if min_price is not None:
            #     min_price = float(min_price)
            # if nb_star is not None:
            #     nb_star = int(nb_star)
        except ValueError:
            return Response('Invalid data format', status=status.HTTP_400_BAD_REQUEST)

        list_hotels = []
        with connection.cursor() as cursor:
            if destination and checkin and checkout:
                if amenities is None and max_price is None and min_price is None and nb_star is None:
                    cursor.callproc('find_available_hotels', [destination, checkin, checkout])
                elif amenities is not None and max_price is not None and min_price is not None and nb_star is not None:
                    cursor.callproc('find_available_hotels_amenities_price_star',
                                    [destination, checkin, checkout, amenities, min_price, max_price, nb_star])
                elif amenities is not None and max_price is None and min_price is None and nb_star is None:
                    cursor.callproc('find_available_hotels_amenities', [destination, checkin, checkout, amenities])
                elif amenities is not None and max_price is not None and min_price is not None and nb_star is None:
                    cursor.callproc('find_available_hotels_price_amenity',
                                    [destination, checkin, checkout, min_price, max_price, amenities])
                elif amenities is not None and max_price is None and min_price is None and nb_star is not None:
                    cursor.callproc('find_available_hotels_amenities_star',
                                    [destination, checkin, checkout, amenities, nb_star])
                elif amenities is None and max_price is not None and min_price is not None and nb_star is not None:
                    cursor.callproc('find_available_hotels_price_star',
                                    [destination, checkin, checkout, min_price, max_price, nb_star])
                elif amenities is None and max_price is not None and min_price is not None and nb_star is None:
                    cursor.callproc('find_available_hotels_price',
                                    [destination, checkin, checkout, min_price, max_price])
                else:
                    cursor.callproc('find_available_hotels_star', [destination, checkin, checkout, nb_star])

                for row in cursor.fetchall():
                    hotel = Hotel(
                        id=row[0],
                        name=row[1],
                        location=row[2],
                        ville=row[3],
                        email=row[4],
                        phone_num=row[5],
                        description=row[6],
                        nb_star=row[7]
                    )
                    list_hotels.append(hotel)

        serializer = HotelSerializer(list_hotels, many=True)
        return Response({'hotel': serializer.data, 'message': 'success'}, status=status.HTTP_200_OK)


class AvailableRooms(APIView):
    def get(self, request):
        id_hotel = request.query_params.get('id_hotel')
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')

        try:
            checkin = datetime.strptime(checkin, "%Y-%m-%d")
            checkout = datetime.strptime(checkout, "%Y-%m-%d")
        except ValueError:
            return Response('Invalid data format', status=status.HTTP_400_BAD_REQUEST)

        list_rooms = []
        with connection.cursor() as cursor:
            if id_hotel is not None and checkin is not None and checkout is not None:
                cursor.callproc('FindAllRoomAvailableInHotel', [id_hotel, checkin, checkout])
                for row in cursor.fetchall():
                    room = {
                        'room_type': row[0],
                        'available_rooms': row[1],
                        'price':row[2]
                    }
                    list_rooms.append(room)

        return Response({'message':'success' , 'list_rooms': list_rooms}, status=status.HTTP_200_OK)
