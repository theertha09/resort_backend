from rest_framework import serializers
from .models import FormData, FormDataImages,WelcomeSection,whychoose, SubscriptionBenefit, SubscriptionPlan, Payment

class FormDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDataImages
        fields = ['id', 'image']

class FormDataSerializer(serializers.ModelSerializer):
    multiple_images = FormDataImagesSerializer(many=True, read_only=True)
    multiple_images_upload = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = FormData
        fields = ['id', 'logo', 'title', 'image', 'description', 'multiple_images', 'multiple_images_upload']

    def create(self, validated_data):
        multiple_images = validated_data.pop('multiple_images_upload', [])
        form_data = FormData.objects.create(**validated_data)
        for image in multiple_images:
            FormDataImages.objects.create(form_data=form_data, image=image)
        return form_data


class WelcomeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeSection
        fields = '__all__'
class whychooseSerializer(serializers.ModelSerializer):
    class Meta:
        model = whychoose
        fields = '__all__'

class FormDataDetailSerializer(serializers.ModelSerializer):
    form_images = FormDataImagesSerializer(many=True, read_only=True)
    welcome_sections = WelcomeSectionSerializer(many=True, read_only=True)
    why_choose_items = whychooseSerializer(many=True, read_only=True)
    class Meta:
        model = FormData
        fields = ['id', 'logo', 'title', 'image', 'description',
                  'form_images', 'welcome_sections', 'why_choose_items']



class FormDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDataImages
        fields = ['id', 'image']

class WelcomeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeSection
        fields = '__all__'

class SubscriptionBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionBenefit
        fields = ['id', 'plan', 'benefit_text']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    benefits = SubscriptionBenefitSerializer(many=True, read_only=True)
    
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'original_price', 'offer_price', 'description', 
                 'is_popular', 'limited_offer', 'benefits']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user_uuid', 'resort', 'subscription_plan', 'amount', 
                 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 
                 'status', 'created_at', 'updated_at']
        read_only_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 
                          'status', 'created_at', 'updated_at']
