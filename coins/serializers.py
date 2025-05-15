from rest_framework import serializers
from .models import Referral

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }
