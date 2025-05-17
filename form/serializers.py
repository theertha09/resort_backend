from rest_framework import serializers
from .models import form  # Consider renaming this model to Form (capitalized) to follow naming conventions
from product.models import Resort

class FormSerializer(serializers.ModelSerializer):
    resort_name = serializers.CharField(source='resort.name', read_only=True)  # Optional: display resort name

    class Meta:
        model = form
        fields = [
            'id',
            'resort',
            'resort_name',  # Optional field
            'name',
            'email',
            'phone_number',
            'location',
            'check_in',
        ]
