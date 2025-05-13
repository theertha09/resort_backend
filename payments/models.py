from django.db import models

# Create your models here.
import uuid
from django.db import models
from login.models import form  # Assuming the form model is in the login app
from properties.models import FormData  # Assuming the FormData model is in the properties app
class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=PLAN_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_popular = models.BooleanField(default=False)
    limited_offer = models.BooleanField(default=False)
    referral_limit = models.IntegerField(null=True, blank=True)  # Null means unlimited

    def __str__(self):
        return self.name.capitalize()

class SubscriptionBenefit(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='benefits')
    benefit_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.plan.name.capitalize()}: {self.benefit_text}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(form, on_delete=models.CASCADE, null=True, blank=True)
    resort = models.ForeignKey(FormData, on_delete=models.CASCADE, null=True, blank=True)  
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='paid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

