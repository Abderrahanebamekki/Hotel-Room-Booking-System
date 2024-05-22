from django.urls import path,include

from hotel.views import Search, AvailableRooms

urlpatterns = [
    path('search/', Search.as_view(), name='search'),
    path('availableRooms/' , AvailableRooms.as_view(), name='availableRooms')
]