# points/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Points
from .serializers import PointsNumberSerializer

class PointsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Points.objects.all()
    serializer_class = PointsNumberSerializer
    permission_classes = [AllowAny]

class PointsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Points.objects.all()
    serializer_class = PointsNumberSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'  # optional, default is 'pk' (id)
