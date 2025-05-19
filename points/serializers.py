from rest_framework import serializers
from .models import Points
from login.models import form  # Assuming your user model is named 'form'

class PointsNumberSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)
    points = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Points
        fields = ['id', 'user_uuid', 'points']

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
            'points': str(instance.points)  # Ensures decimal is returned as a string
        }
