from rest_framework import serializers
from .models import Resort, State, Property, Feature, WhatToExpect


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']



class WhatToExpectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatToExpect
        fields = ['id', 'content']


class ResortSerializer(serializers.ModelSerializer):
    place = StateSerializer(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), write_only=True, source='place')

    features = FeatureSerializer(many=True, read_only=True)
    properties = PropertySerializer(many=True, read_only=True)
    what_to_expect = WhatToExpectSerializer(many=True, read_only=True)

    features_ids = serializers.CharField(write_only=True, required=False)
    properties_ids = serializers.CharField(write_only=True, required=False)
    what_to_expect_contents = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Resort
        fields = ['id', 'name', 'location', 'image', 'place', 'place_id',
                  'description', 'price', 'is_featured',
                  'features', 'properties', 'what_to_expect','actual_price',
                  'features_ids', 'properties_ids', 'what_to_expect_contents']

    def create(self, validated_data):
        features_str = validated_data.pop('features_ids', '')
        properties_str = validated_data.pop('properties_ids', '')
        what_to_expect_contents = validated_data.pop('what_to_expect_contents', [])

        resort = Resort.objects.create(**validated_data)

        if features_str:
            feature_ids = [int(pk.strip()) for pk in features_str.split(',') if pk.strip()]
            resort.features.set(feature_ids)

        if properties_str:
            property_ids = [int(pk.strip()) for pk in properties_str.split(',') if pk.strip()]
            resort.properties.set(property_ids)

        for content in what_to_expect_contents:
            WhatToExpect.objects.create(resort=resort, content=content)

        return resort

    def update(self, instance, validated_data):
        features_str = validated_data.pop('features_ids', None)
        properties_str = validated_data.pop('properties_ids', None)
        what_to_expect_contents = validated_data.pop('what_to_expect_contents', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if features_str is not None:
            feature_ids = [int(pk.strip()) for pk in features_str.split(',') if pk.strip()]
            instance.features.set(feature_ids)

        if properties_str is not None:
            property_ids = [int(pk.strip()) for pk in properties_str.split(',') if pk.strip()]
            instance.properties.set(property_ids)

        if what_to_expect_contents is not None:
            instance.what_to_expect.all().delete()
            for content in what_to_expect_contents:
                WhatToExpect.objects.create(resort=instance, content=content)

        return instance
