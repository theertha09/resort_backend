from rest_framework import serializers
from .models import PhoneNumber

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone_number']  # Specify the fields to include in the API response

    def create(self, validated_data):
        """Override the create method to customize object creation."""
        return PhoneNumber.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Override the update method to customize object updates."""
        instance.phone_numbers = validated_data.get('phone_numbers', instance.phone_numbers)
        instance.save()
        return instance
