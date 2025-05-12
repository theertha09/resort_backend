import uuid
from django.db import models
from login.models import form  # Assuming the form model is in the login app

class FormData(models.Model):

    TYPE_CHOICES = (
        ('static', 'Static'),
        ('partner', 'Partner'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logo = models.ImageField(upload_to='form/logo/')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='form/main_image/')
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # 👈 Add this

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
    

    def __str__(self):
        return self.title

class FormDataImages(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE, related_name='multiple_images')
    image = models.ImageField(upload_to='form/multiple_images/')

class FormDataImages(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE, related_name='form_images')
    image = models.ImageField(upload_to='form/multiple_images/')

class WelcomeSection(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE, related_name='welcome_sections')
    title = models.CharField(max_length=200)
    highlight = models.CharField(max_length=100)
    subtitle = models.TextField()
    image_url = models.URLField()

class whychoose(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE, related_name='why_choose_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()

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

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(form, on_delete=models.CASCADE)
    resort = models.ForeignKey(FormData, on_delete=models.CASCADE)  
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

