
from django.db import models



class Property(models.Model):  # Make sure this exists
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Feature(models.Model):  # Make sure this exists
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resort(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='resorts/', blank=True, null=True)
    place = models.ForeignKey(State, on_delete=models.CASCADE, related_name='resorts')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    properties = models.ManyToManyField('Property', blank=True, related_name='resorts')  # corrected
    features = models.ManyToManyField('Feature', blank=True, related_name='resorts')    # corrected
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return self.name



class WhatToExpect(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='what_to_expect')
    content = models.TextField()

    def __str__(self):
        return self.content[:50]  # show first 50 chars
