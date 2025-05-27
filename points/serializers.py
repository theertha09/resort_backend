from rest_framework import serializers
from .models import Points
from login.models import form

class PointsNumberSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Points
        fields = ['id', 'user_uuid', 'points', 'is_redeemed', 'status']

    def create(self, validated_data):
        user_uuid = validated_data.pop('user_uuid')
        try:
            user = form.objects.get(uuid=user_uuid)
        except form.DoesNotExist:
            raise serializers.ValidationError("User with this UUID does not exist.")
        
        validated_data['user'] = user
        return Points.objects.create(**validated_data)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user_uuid': str(instance.user.uuid),
            'points': str(instance.points),
            'is_redeemed': instance.is_redeemed,
            'status': instance.status,
        }
