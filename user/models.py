from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=50)
    username = models.EmailField(max_length=255, unique=True , null= True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username if self.username else 'No Username'

class Client (models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50 , null=False)
    email = models.EmailField(max_length=255 , unique= True)
    phone = models.CharField(max_length=50, null= False)
    address = models.CharField(max_length=50, null= False)
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)

