from django.db import models
from login.models import form  # Assuming your custom user model is 'form'

class Points(models.Model):  # Model name in PascalCase
    user = models.ForeignKey(form, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=2)
    is_redemmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)  # Adjust if 'form' has 'full_name'
