from rest_framework import serializers
from .models import FormData, FormDataImages,WelcomeSection,whychoose

class FormDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDataImages
        fields = ['id', 'image']

class FormDataSerializer(serializers.ModelSerializer):
    resort_name = serializers.CharField(source='resort.name', read_only=True)
    resort_location = serializers.CharField(source='resort.location', read_only=True)  # ✅ NEW

    multiple_images = FormDataImagesSerializer(many=True, read_only=True)
    multiple_images_upload = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = FormData
        fields = [
            'id',
            'logo',
            'title',
            'image',
            'description',
            'resort',           # for sending resort ID when creating/updating
            'resort_name',      # read-only: display resort name
            'resort_location',  # ✅ read-only: display resort location
            'multiple_images',
            'multiple_images_upload'
        ]

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
    resort_name = serializers.CharField(source='resort.name', read_only=True)
    resort_location = serializers.CharField(source='resort.location', read_only=True)

    form_images = FormDataImagesSerializer(many=True, read_only=True)
    welcome_sections = WelcomeSectionSerializer(many=True, read_only=True)
    why_choose_items = whychooseSerializer(many=True, read_only=True)

    class Meta:
        model = FormData
        fields = [
            'id', 'logo', 'title', 'image', 'description',
            'resort_name', 'resort_location',  # ✅ Add these fields
            'form_images', 'welcome_sections', 'why_choose_items',
        ]


class FormDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDataImages
        fields = ['id', 'image']

class WelcomeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeSection
        fields = '__all__'

