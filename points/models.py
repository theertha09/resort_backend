from django.db import models
from login.models import form  # Consider renaming 'form' to 'Form' for clarity

# Create your models here.
class points(models.Model):  # Correct PascalCase
    user = models.ForeignKey(form, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.full_name
