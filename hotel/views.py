from _datetime import datetime

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
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')
        amenities = request.query_params.get('amenities')
        max_price = request.query_params.get('max_price')
        min_price = request.query_params.get('min_price')
        nb_star = request.query_params.get('nb_star')
        try:
            # Attempt to convert the string to a date object using the "%Y-%m-%d" format
            checkin = datetime.strptime(checkin, "%Y-%m-%d")
            checkout = datetime.strptime(checkout, "%Y-%m-%d")
            if max_price is not None and min_price is not None:
                max_price = float(max_price)
                min_price = float(min_price)
            if nb_star is not None:
              nb_star = int(nb_star)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
        print(type(checkout))

        list_hotels = []
        with connection.cursor() as cursor:
            if destination and checkin and checkout:
                if amenities is  None and max_price is  None and min_price is  None and nb_star is None:
                    cursor.callproc('find_available_hotels',[destination, checkin, checkout])
                elif amenities is not None and max_price is not None and min_price is not None and nb_star is not None:
                    cursor.callproc('find_available_hotels_amenities_price_star', [destination, checkin, checkout, amenities, min_price, max_price, nb_star])
                elif amenities is not None and max_price is None and min_price is None and nb_star is None:
                    cursor.callproc('find_available_hotels_amenities', [destination, checkin, checkout, amenities])
                elif destination is not None and checkin is not None and checkout is not None and amenities is not None and max_price is not None and min_price is not None and nb_star is None:
                    cursor.callproc('find_available_hotels_price_amenity', [destination, checkin, checkout, min_price, max_price,amenities])
                elif amenities is not None and max_price is  None and min_price is  None and nb_star is not None:
                    cursor.callproc('find_available_hotels_amenities_star', [destination, checkin, checkout, amenities,nb_star])
                elif amenities is  None and max_price is not None and min_price is not None and nb_star is not None:
                    cursor.callproc('find_available_hotels_price_star', [destination, checkin, checkout,min_price, max_price,nb_star])
                elif destination is not None and checkin is not None and checkout is not None and amenities is  None and max_price is not None and min_price is not None and nb_star is None:
                    cursor.callproc('find_available_hotels_price', [destination, checkin, checkout,min_price, max_price])
                else:
                    cursor.callproc('find_available_hotels_star', [destination, checkin, checkout,nb_star])
                for row in cursor.fetchall():
                    hotel_data = {}
                    for idx, field in enumerate(
                            ['id', 'name', 'location', 'ville', 'address', 'email', 'telephone', 'description',
                             'nb_star']):
                        hotel_data[field] = row[idx]
                    list_hotels.append(hotel_data)




        # Return the serialized data as response
        return Response(list_hotels, status=status.HTTP_200_OK)