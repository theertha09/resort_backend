from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Resort, State, Property, Feature
from .serializers import ResortSerializer, StateSerializer, PropertySerializer, FeatureSerializer

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
