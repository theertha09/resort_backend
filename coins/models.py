from django.db import models
from login.models import form  # Assuming 'form' is the user model
import uuid

class Referral(models.Model):
    user = models.ForeignKey(form, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name  # Fixed from self.full_name
