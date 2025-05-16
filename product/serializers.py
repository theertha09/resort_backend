# resorts/serializers.py

from rest_framework import serializers
from .models import Resort, State

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class ResortSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = Resort
        fields = ['id', 'name', 'location', 'image', 'state', 'description','price']
