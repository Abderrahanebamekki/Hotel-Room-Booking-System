from django.urls import path,include

from booking.views import GetBookingsView , BookingRoomView

urlpatterns = [
    path('book/', BookingRoomView.as_view(), name='bookings')
]