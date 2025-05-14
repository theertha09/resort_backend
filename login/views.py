from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import form
from .serializers import FormSerializer 
from drf_yasg import openapi
from rest_framework.permissions import AllowAny





# View for form model
class FormListCreateAPIView(generics.ListCreateAPIView):
    queryset = form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [AllowAny]  # Allow access without authentication



class FormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'uuid'
    permission_classes = [AllowAny]
