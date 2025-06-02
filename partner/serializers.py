from rest_framework import serializers
from .models import Property, PropertyPhoto

# serializers.py
class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ['id', 'image']

class PropertySerializer(serializers.ModelSerializer):
    photos = PropertyPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'name',
            'property_type',
            'location',
            'contact_person',
            'phone_number',
            'email',
            'photos'  # Include this!
        ]

from rest_framework import serializers
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
