from rest_framework import serializers
from .models import SubscriptionPlan, SubscriptionBenefit

class SubscriptionBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionBenefit
        fields = ['id', 'benefit_text']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    benefits = SubscriptionBenefitSerializer(many=True, required=False)  # Allow benefits to be added

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'original_price', 'offer_price', 'description',
            'is_popular', 'limited_offer', 'benefits'
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
