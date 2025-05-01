from django.shortcuts import render

# Create your views here.
# resorts/views.py

from rest_framework import generics
from .models import Resort, State
from .serializers import ResortSerializer, StateSerializer

class StateListAPIView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class ResortListAPIView(generics.ListAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        state_id = self.request.query_params.get('state_id')
        if state_id:
            queryset = queryset.filter(state__id=state_id)
        return queryset

class ResortDetailAPIView(generics.RetrieveAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = 'id'
