# user/models.py

from django.db import models

class PhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)  # Custom ID field

    phone_number = models.CharField(max_length=15)  # Or the correct field name and type

    def __str__(self):
        return f"Phone Number: {self.phone_number}"
