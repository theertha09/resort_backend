from django.db import models
from login.models import form  # Consider renaming 'form' to 'Form' for clarity

class Address(models.Model):
    user = models.ForeignKey(form, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='addresses/', null=True, blank=True)

    def __str__(self):
        return str(self.user)  # Ensure string representation is valid
