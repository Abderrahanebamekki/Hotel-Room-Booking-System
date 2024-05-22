from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField(max_length=500, null=True)  # Use PointField for geographical coordinates
    ville = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_num = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(default='')
    nb_star = models.IntegerField(default=0)

class Images(models.Model):
    image = models.TextField(null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE , null=True)
class RoomType(models.Model):
    name = models.CharField(max_length=50)

class bed(models.Model):
    type = models.CharField(max_length=50)

class Room(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nb_bed = models.IntegerField(default=0)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    bed = models.ForeignKey(bed, on_delete=models.CASCADE, null=True)
class Amenity(models.Model):
    name = models.CharField(max_length=50)
class AmenityRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, null=True)
class AmenityHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, null=True)


