from django.db import models

# Create your models here.
from django.db import models

class Reservation(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.CharField(max_length=10)  # "1 Guest", "2 Guests", etc.
    special_requests = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.check_in_date} to {self.check_out_date})"
