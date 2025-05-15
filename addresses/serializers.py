from rest_framework import serializers
from .models import Address
from login.models import form

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = form
        fields = ['full_name', 'dob', 'email', 'phone_number', 'gender']

class AddressSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(source='user', read_only=True)
    user_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Address
        fields = ['id', 'user_uuid', 'user_details', 'address', 'image']

    def create(self, validated_data):
        uuid = validated_data.pop('user_uuid')
        user_instance = form.objects.get(uuid=uuid)
        return Address.objects.create(user=user_instance, **validated_data)
