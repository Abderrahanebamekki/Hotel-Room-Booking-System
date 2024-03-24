from django.db import models
from user.models import Client
from hotel.models import Room

# Create your models here.


class Booking(models.Model):
    client = models.ForeignKey(Client, related_name='client',on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=False)
    check_out = models.DateTimeField(auto_now_add=False)
    num_adults = models.IntegerField(default=1)
    num_children = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0)

class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, related_name='booking',on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='booking_rooms',on_delete=models.CASCADE)


