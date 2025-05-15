# from rest_framework import serializers
# from .models import address, Referral
# from login.models import form
# from rest_framework import serializers

# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = form
#         fields = ['user_uuid', 'full_name', 'email', 'phone_number', 'gender']

# class addressSerializer(serializers.ModelSerializer):
#     user_details = UserDetailsSerializer(source='user_uuid', read_only=True)
#     user_uuid = serializers.UUIDField(write_only=True)

#     class Meta:
#         model = address
#         fields = ['id', 'user_uuid', 'user_details', 'address']

#     def create(self, validated_data):
#         user_uuid = validated_data.pop('user_uuid')
#         user_instance = form.objects.get(user_uuid=user_uuid)
#         return address.objects.create(user_uuid=user_instance, **validated_data)
