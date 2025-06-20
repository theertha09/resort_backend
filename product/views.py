from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Resort, State, Property, Feature
from .serializers import ResortSerializer, StateSerializer, PropertySerializer, FeatureSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

# STATE VIEWS
class StateListCreateAPIView(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class StateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'id'
    authentication_classes = []
    permission_classes = [AllowAny]

# RESORT VIEWS
class ResortListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResortSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Resort.objects.all()
        state_id = self.request.query_params.get('state_id')
        if state_id:
            queryset = queryset.filter(place__id=state_id)  # Corrected to 'place' if you're using ForeignKey to State
        return queryset

class ResortRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = 'id'
    authentication_classes = []
    permission_classes = [AllowAny]

# PROPERTY VIEWS
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    authentication_classes = []
    permission_classes = [AllowAny]

# FEATURE VIEWS
class FeatureListCreateView(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

class FeatureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
class ResortCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    parser_classes = [MultiPartParser, FormParser]


# class ResortFeatureRemoveAPIView(APIView):
#     permission_classes = [AllowAny]
#     def delete(self, request, resort_id):
#         feature_ids = request.data.get('feature_ids', [])

#         if not isinstance(feature_ids, list) or not all(isinstance(i, int) for i in feature_ids):
#             return Response({
#                 "code": 400,
#                 "message": "feature_ids must be a list of integers."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             resort = Resort.objects.get(id=resort_id)
#         except Resort.DoesNotExist:
#             raise NotFound(detail="Resort not found")

#         # Filter and remove only valid feature IDs
#         existing_ids = resort.features.values_list('id', flat=True)
#         valid_ids = set(existing_ids).intersection(feature_ids)
#         resort.features.remove(*valid_ids)

#         return Response({
#             "code": 200,
#             "message": "Features removed successfully"
#         }, status=status.HTTP_200_OK)



class ResortFeaturePropertyRemoveAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, resort_id):
        feature_ids = request.data.get('feature_ids', [])
        property_ids = request.data.get('properties_ids', [])

        # Validate input
        if feature_ids and (not isinstance(feature_ids, list) or not all(isinstance(i, int) for i in feature_ids)):
            return Response({
                "code": 400,
                "message": "feature_ids must be a list of integers."
            }, status=status.HTTP_400_BAD_REQUEST)

        if property_ids and (not isinstance(property_ids, list) or not all(isinstance(i, int) for i in property_ids)):
            return Response({
                "code": 400,
                "message": "properties_ids must be a list of integers."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            resort = Resort.objects.get(id=resort_id)
        except Resort.DoesNotExist:
            raise NotFound(detail="Resort not found")

        # Remove features if provided
        if feature_ids:
            existing_feature_ids = set(resort.features.values_list('id', flat=True))
            valid_feature_ids = existing_feature_ids.intersection(feature_ids)
            resort.features.remove(*valid_feature_ids)

        # Remove properties if provided
        if property_ids:
            existing_property_ids = set(resort.properties.values_list('id', flat=True))
            valid_property_ids = existing_property_ids.intersection(property_ids)
            resort.properties.remove(*valid_property_ids)

        return Response({
            "code": 200,
            "message": "Features and/or properties removed successfully"
        }, status=status.HTTP_200_OK)
