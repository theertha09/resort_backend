from django.db import models

# Create your models here.
import uuid
from django.db import models

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=PLAN_CHOICES, unique=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_popular = models.BooleanField(default=False)
    limited_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name.capitalize()

class SubscriptionBenefit(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='benefits')
    benefit_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.plan.name.capitalize()}: {self.benefit_text}"
