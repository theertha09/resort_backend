from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from .models import Property, PropertyPhoto
from .serializers import PropertySerializer

class PropertyRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        images = request.FILES.getlist('photos')

        if len(images) > 3:
            return Response({"error": "You can upload up to 3 images only."}, status=400)

        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    property_instance = serializer.save()
                    for image in images:
                        PropertyPhoto.objects.create(property=property_instance, image=image)
                return Response({
                    "message": "Property registered successfully.",
                    "property_id": property_instance.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
    def get(self, request, *args, **kwargs):
            properties = Property.objects.all()
            serializer = PropertySerializer(properties, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework import generics
from .models import Content
from .serializers import ContentSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Content
from .serializers import ContentSerializer

class ContentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication

class ContentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication
