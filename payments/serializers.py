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
            'uuid', 'name', 'amount', 'description',
            'is_popular', 'limited_offer', 'benefits','referral_limit',
        ]

    def create(self, validated_data):
        benefits_data = validated_data.pop('benefits', [])
        subscription_plan = SubscriptionPlan.objects.create(**validated_data)
        
        # Create associated benefits if any
        for benefit_data in benefits_data:
            SubscriptionBenefit.objects.create(plan=subscription_plan, **benefit_data)
        
        return subscription_plan

    def create(self, validated_data):
        benefits_data = validated_data.pop('benefits', [])
        subscription_plan = SubscriptionPlan.objects.create(**validated_data)

        # Avoid duplicate benefits
        seen_texts = set()
        for benefit_data in benefits_data:
            benefit_text = benefit_data.get('benefit_text')
            if benefit_text and benefit_text not in seen_texts:
                seen_texts.add(benefit_text)
                SubscriptionBenefit.objects.create(plan=subscription_plan, benefit_text=benefit_text)

        return subscription_plan

    def update(self, instance, validated_data):
        benefits_data = validated_data.pop('benefits', [])

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Track existing and incoming benefits
        existing_benefits = {b.id: b for b in SubscriptionBenefit.objects.filter(plan=instance)}
        seen_texts = set()

        for benefit_data in benefits_data:
            benefit_text = benefit_data.get('benefit_text')
            benefit_id = benefit_data.get('id')

            if benefit_text in seen_texts:
                continue  # Skip duplicates in incoming data
            seen_texts.add(benefit_text)

            if benefit_id and benefit_id in existing_benefits:
                benefit = existing_benefits[benefit_id]
                benefit.benefit_text = benefit_text
                benefit.save()
            elif not benefit_id:
                # Prevent creating duplicate benefit_text
                if not SubscriptionBenefit.objects.filter(plan=instance, benefit_text=benefit_text).exists():
                    SubscriptionBenefit.objects.create(plan=instance, benefit_text=benefit_text)

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