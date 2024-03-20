from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    username = None
    password = models.CharField(max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Client (models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50 , null=False)
    email = models.EmailField(max_length=255 , unique= True)
    phone = models.CharField(max_length=50, null= False)
    address = models.CharField(max_length=50, null= False)

