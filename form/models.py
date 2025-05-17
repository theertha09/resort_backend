from django.db import models

# Create your models here.
from django.db import models
from login.models import form  # Consider renaming 'form' to 'Form' for clarity
from product.models import Resort  # Ensure this import is correct
class form(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    check_in = models.DateField()
    def __str__(self):
        return str(self.user)  # Ensure string representation is valid
