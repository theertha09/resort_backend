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

    def __str__(self):
        return self.title