from django.contrib.auth.models import  User, UserManager
from django.db import models

class CustomUser (User) :
    typeUser = models.CharField(max_length= 20)
    fullname = models.CharField(max_length= 30)
    objects = UserManager()