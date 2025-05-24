# serializers.py
from rest_framework import serializers
from .models import form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = form
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return data

class SetInitialPasswordSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return data

class ResetPasswordSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return data
