from django.db import models
from login.models import form  # Assuming 'form' is the correct model name from the login app
# Create your models here.
class Referral(models.Model):
    user = models.ForeignKey(form, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
              return self.full_name