# resorts/serializers.py

from rest_framework import serializers
from .models import Resort, State

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class ResortSerializer(serializers.ModelSerializer):
    place = StateSerializer(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(), write_only=True, source='place'
    )

    class Meta:
        model = Resort
        fields = ['id', 'name', 'location', 'image', 'place', 'place_id', 'description','price','is_featured']
