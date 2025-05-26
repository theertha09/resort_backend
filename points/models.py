from django.db import models
from login.models import form  # Assuming your custom user model is 'form'

class Points(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(form, on_delete=models.CASCADE, related_name='points')
    points = models.DecimalField(max_digits=10, decimal_places=2)
    is_redeemed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # ✅ status field
  
    def __str__(self):
        return f"{self.user} - {self.points} points - {self.status}"
