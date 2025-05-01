# serializers.py
from rest_framework import serializers
from .models import form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = form
        fields = '__all__'

