import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from hotel.models import Hotel
from hotel.serializer import HotelSerializer


# Create your views here.



# class Search(APIView):
#     def get(self, request):
#         # Retrieve data from request body
#         destination = request.data.get('destination')
#         check_in_date = request.data.get('check_in')
#         check_out_date = request.data.get('check_out')
#         amenities_list = request.data.get('amenities', [])
#         amenities = ','.join(amenities_list)          # convert amenities_list to a string with
#
#
#
#         with connection.cursor() as cursor:
#             cursor.callproc('getHotels', [destination, check_in_date, check_out_date, amenities])
#             list_hotels =  cursor.fetchall()
#
#
#
#
#
#         return Response(list_hotels)



class Search(APIView):
    def get(self, request):
        # Retrieve data from request query parameters
        destination = request.query_params.get('destination')

        if destination is None:
            return Response({"error": "Destination is required"}, status=400)


        hotels = Hotel.objects.filter(ville=destination)

        # Serialize the queryset
        serializer = HotelSerializer(hotels, many=True)

        # Return the serialized data as response
        return Response(serializer.data)