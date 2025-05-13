from rest_framework import serializers
from .models import points

class pointsNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = points
        fields = ['id', 'phone_number']  