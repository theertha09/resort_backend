from rest_framework import serializers
from .models import Referral
from login.models import form  # assuming this is your custom user model

class ReferralSerializer(serializers.ModelSerializer):
    user_uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Referral
        fields = ['id', 'user_uuid', 'email','name','phone_number']  # Add fields as needed
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def get_user_uuid(self, obj):
        return str(obj.user.uuid) if obj.user and hasattr(obj.user, 'uuid') else None
