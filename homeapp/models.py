from django.db import models

# Create your models here.

class User_data(models.Model):
    username = models.CharField(max_length=122)
    password = models.CharField(max_length=122)
    course = models.CharField(max_length=122)
    amount = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12, default="")