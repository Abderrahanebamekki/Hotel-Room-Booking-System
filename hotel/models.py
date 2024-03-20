from django.db import models

# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField(max_length=500 , null= True)  # Use PointField for geographical coordinates
    ville = models.CharField(max_length=100)
    address = models.TextField()
    email = models.CharField(max_length=100 , null=True, blank=True)
    telephone = models.CharField(max_length=100 , null=True, blank=True)

class AmenityHotel(models.Model):
    nbr_etoiles = models.PositiveIntegerField(null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE , related_name='hotel' , null= True)



class RoomType(models.Model):
    name = models.CharField(max_length=50)



class AmenityRoom(models.Model):
    name = models.CharField(max_length=50)

class AmenitiesType:
    typeRoom = models.ForeignKey(RoomType, related_name='type_room', on_delete=models.CASCADE)
    amenity = models.ForeignKey(AmenityRoom, related_name='amenity', on_delete=models.CASCADE)
class Room(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE)
    nbr_bed = models.PositiveIntegerField(default=0)
    room_type = models.ForeignKey(RoomType,related_name='room_type' ,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
class Bed(models.Model):
    nom = models.CharField(max_length=50)

class Bed_type(models.Model):
    bed = models.ForeignKey(Bed,related_name='bed' ,on_delete=models.CASCADE)
    room = models.ForeignKey(Room , related_name='room' ,on_delete=models.CASCADE)


















