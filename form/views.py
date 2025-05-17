from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import form  # Still consider renaming to Form
from .serializers import FormSerializer

class FormListCreateAPIView(generics.ListCreateAPIView):
    queryset = form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [AllowAny]

class FormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [AllowAny]
