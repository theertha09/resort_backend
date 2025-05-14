from rest_framework import serializers
from .models import Referral
from login.models import form
from rest_framework import serializers



class BulkReferralSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Referral
        fields = ['id','user_uuid', 'name', 'email', 'phone_number']

    def create(self, validated_data):
        user_uuid = validated_data.pop('user_uuid')
        try:
            user = form.objects.get(uuid=user_uuid)  # ✅ use 'uuid' instead of 'user_uuid'
        except form.DoesNotExist:
            raise serializers.ValidationError("Invalid user_uuid")
        return Referral.objects.create(user=user, **validated_data)

    def create_bulk(self, validated_data_list):
        objects = []
        for item in validated_data_list:
            user_uuid = item.pop('user_uuid')
            try:
                user = form.objects.get(uuid=user_uuid)  # ✅ correct field
            except form.DoesNotExist:
                raise serializers.ValidationError("Invalid user_uuid")
            objects.append(Referral(user=user, **item))
        return Referral.objects.bulk_create(objects)

    def save(self, **kwargs):
        if isinstance(self.validated_data, list):
            return self.create_bulk(self.validated_data)
        return super().save(**kwargs)
