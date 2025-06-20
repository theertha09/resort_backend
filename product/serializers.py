from rest_framework import serializers
from .models import Resort, State, Property, Feature, WhatToExpect
from rest_framework.exceptions import ValidationError


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

    class Meta:
        model = Resort
        fields = [
            'id', 'name', 'location', 'image', 'place', 'place_id',
            'description', 'price', 'is_featured', 'features', 'properties',
            'what_to_expect', 'actual_price', 'features_ids', 'properties_ids'
        ]

    def get_expectation_contents(self):
        request = self.context.get('request')
        if not request:
            return []
        data = request.data
        return [
            value for key, value in data.items()
            if key.startswith('what_to_expect_contents_') and value.strip()
        ]

class ResortSerializer(serializers.ModelSerializer):
    place = StateSerializer(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), write_only=True, source='place')

    features = FeatureSerializer(many=True, read_only=True)
    properties = PropertySerializer(many=True, read_only=True)
    what_to_expect = serializers.SerializerMethodField()

    features_ids = serializers.CharField(write_only=True, required=False)
    properties_ids = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Resort
        fields = [
            'id', 'name', 'location', 'image', 'place', 'place_id',
            'description', 'price', 'is_featured', 'features', 'properties',
            'what_to_expect', 'actual_price', 'features_ids', 'properties_ids'
        ]

    def get_expectation_contents(self):
        request = self.context.get('request')
        if not request:
            return {}
        data = request.data
        expectations = {}
        for key, value in data.items():
            if key.startswith('what_to_expect_contents_'):
                try:
                    index = int(key.split('_')[-1])
                    if index >= 1 and value.strip():
                        expectations[index] = value.strip()
                except ValueError:
                    continue
        return dict(sorted(expectations.items()))

    def create(self, validated_data):
        features_str = validated_data.pop('features_ids', '')
        properties_str = validated_data.pop('properties_ids', '')
        expectation_contents = self.get_expectation_contents()

        feature_ids = [int(pk.strip()) for pk in features_str.split(',') if pk.strip()] if features_str else []
        property_ids = [int(pk.strip()) for pk in properties_str.split(',') if pk.strip()] if properties_str else []

        invalid_features = set(feature_ids) - set(Feature.objects.filter(id__in=feature_ids).values_list('id', flat=True))
        if invalid_features:
            raise ValidationError({"features_ids": f"Invalid Feature IDs: {list(invalid_features)}"})

        invalid_properties = set(property_ids) - set(Property.objects.filter(id__in=property_ids).values_list('id', flat=True))
        if invalid_properties:
            raise ValidationError({"properties_ids": f"Invalid Property IDs: {list(invalid_properties)}"})

        resort = Resort.objects.create(**validated_data)

        if feature_ids:
            resort.features.set(feature_ids)
        if property_ids:
            resort.properties.set(property_ids)

        # Save to DB but use manual index for response
        for idx, content in expectation_contents.items():
            WhatToExpect.objects.create(resort=resort, content=content)

        resort._manual_expectation = expectation_contents  # Attach for response method
        return resort

    def update(self, instance, validated_data):
        features_str = validated_data.pop('features_ids', None)
        properties_str = validated_data.pop('properties_ids', None)
        expectation_contents = self.get_expectation_contents()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if features_str is not None:
            new_ids = [int(pk.strip()) for pk in features_str.split(',') if pk.strip()]
            existing_ids = list(instance.features.values_list('id', flat=True))
            combined_ids = list(set(existing_ids + new_ids))
            invalid_features = set(combined_ids) - set(Feature.objects.filter(id__in=combined_ids).values_list('id', flat=True))
            if invalid_features:
                raise ValidationError({"features_ids": f"Invalid Feature IDs: {list(invalid_features)}"})
            instance.features.set(combined_ids)

        if properties_str is not None:
            new_props = [int(pk.strip()) for pk in properties_str.split(',') if pk.strip()]
            existing_props = list(instance.properties.values_list('id', flat=True))
            combined_props = list(set(existing_props + new_props))
            invalid_properties = set(combined_props) - set(Property.objects.filter(id__in=combined_props).values_list('id', flat=True))
            if invalid_properties:
                raise ValidationError({"properties_ids": f"Invalid Property IDs: {list(invalid_properties)}"})
            instance.properties.set(combined_props)

        if expectation_contents:
            instance.what_to_expect.all().delete()
            for idx, content in expectation_contents.items():
                WhatToExpect.objects.create(resort=instance, content=content)
            instance._manual_expectation = expectation_contents  # Attach for response

        return instance

    def get_what_to_expect(self, obj):
        # If manually attached (during create/update), return manual mapping
        if hasattr(obj, '_manual_expectation'):
            return [{"id": idx, "content": content} for idx, content in obj._manual_expectation.items()]
        # Else, return from DB
        return [{"id": idx + 1, "content": w.content} for idx, w in enumerate(obj.what_to_expect.all())]
