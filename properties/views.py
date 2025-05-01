from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from .models import FormData, FormDataImages,WelcomeSection,whychoose
from .serializers import FormDataSerializer, FormDataImagesSerializer,WelcomeSectionSerializer,whychooseSerializer,FormDataDetailSerializer

# Create and List FormData
class FormDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    permission_classes = [AllowAny]

# Retrieve, Update, Delete FormData
class FormDataRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    lookup_field = 'id'  # because UUID
    permission_classes = [AllowAny]

# Upload Multiple Images to FormData
class UploadMultipleImagesAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        try:
            form_data = FormData.objects.get(id=id)
        except FormData.DoesNotExist:
            return Response({"error": "Form data not found"}, status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('images')  # 👈 Important: "images" is key in Postman form-data
        if not images:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded = []
        for img in images:
            image_obj = FormDataImages.objects.create(form_data=form_data, image=img)
            uploaded.append({
                'id': image_obj.id,
                'image_url': request.build_absolute_uri(image_obj.image.url)
            })

        return Response({
            "message": "Images uploaded successfully",
            "images": uploaded
        }, status=status.HTTP_201_CREATED)
class welcometaListCreateAPIView(generics.ListCreateAPIView):
    queryset = WelcomeSection.objects.all()
    serializer_class = WelcomeSectionSerializer
    permission_classes = [AllowAny]

# Retrieve, Update, Delete FormData
class welcomeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WelcomeSection.objects.all()
    serializer_class = WelcomeSectionSerializer
    lookup_field = 'id'  # because UUID
    permission_classes = [AllowAny]

class whychooseListCreateAPIView(generics.ListCreateAPIView):
    queryset = whychoose.objects.all()
    serializer_class = whychooseSerializer
    permission_classes = [AllowAny]

class whychooseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = whychoose.objects.all()
    serializer_class = whychooseSerializer
    lookup_field = 'id'  # because UUID
    permission_classes = [AllowAny]

class FormDataFullDetailAPIView(RetrieveAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataDetailSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
