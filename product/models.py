
from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resort(models.Model):
    user = models.ForeignKey('login.form', on_delete=models.CASCADE, related_name='resorts')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='resorts/')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='resorts')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
