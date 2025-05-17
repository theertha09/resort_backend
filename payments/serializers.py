from rest_framework import serializers
from .models import SubscriptionPlan, SubscriptionBenefit,Payment
from .models import  SubscriptionBenefit, SubscriptionPlan, Payment

class SubscriptionBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionBenefit
        fields = ['id', 'benefit_text']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    benefits = SubscriptionBenefitSerializer(many=True, required=False)  # Allow benefits to be added

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'amount', 'description',
            'is_popular', 'limited_offer', 'benefits','referral_limit',
        ]

    def create(self, validated_data):
        benefits_data = validated_data.pop('benefits', [])
        subscription_plan = SubscriptionPlan.objects.create(**validated_data)
        
        # Create associated benefits if any
        for benefit_data in benefits_data:
            SubscriptionBenefit.objects.create(plan=subscription_plan, **benefit_data)
        
        return subscription_plan

    def update(self, instance, validated_data):
        # Update the subscription plan fields
        benefits_data = validated_data.pop('benefits', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update benefits
        for benefit_data in benefits_data:
            benefit_id = benefit_data.get('id', None)
            if benefit_id:
                # If benefit ID exists, update existing benefit
                benefit = SubscriptionBenefit.objects.get(id=benefit_id, plan=instance)
                benefit.benefit_text = benefit_data['benefit_text']
                benefit.save()
            else:
                # If benefit ID does not exist, create a new benefit
                SubscriptionBenefit.objects.create(plan=instance, **benefit_data)
        
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    user_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'user_uuid', 'subscription_plan', 'amount', 
            'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 
            'status', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 
            'status', 'created_at', 'updated_at'
        ]

    def get_user_uuid(self, obj):
        # Assumes obj.user has a uuid field 
        return str(obj.user.uuid) if obj.user and hasattr(obj.user, 'uuid') else None 