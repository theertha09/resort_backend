from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import points
from .serializers import pointsNumberSerializer

class pointsListCreateAPIView(generics.ListAPIView):
    queryset = points.objects.all()
    serializer_class = pointsNumberSerializer
class pointsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = points.objects.all()
    serializer_class = pointsNumberSerializer