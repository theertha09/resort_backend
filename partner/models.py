from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('homestay', 'Homestay'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_photos/')

    def __str__(self):
        return f"Photo for {self.property.name}"





class Content(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
