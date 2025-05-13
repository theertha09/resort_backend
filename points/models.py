from django.db import models

# Create your models here.
class points(models.Model):  # Correct PascalCase
    amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.full_name
