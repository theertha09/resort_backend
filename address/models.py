
# Create your models here.
from django.db import models
from login.models import form  # Assuming 'form' is the correct model name from the login app
# Create your models here.
class address(models.Model):  # Correct PascalCase
    user = models.ForeignKey(form, on_delete=models.CASCADE, null=True, blank=True)

    address = models.TextField(null=True, blank=True)  # New field

    def __str__(self):
        return self.user
