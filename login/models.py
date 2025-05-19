from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import datetime


class form(models.Model):  # PascalCase naming
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return self.full_name
