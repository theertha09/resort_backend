# from django.shortcuts import render

# # Create your views here.
# from .models import address
# from .serializers import addressSerializer
# from rest_framework.permissions import AllowAny
# from .serializers import addressSerializer
# from rest_framework import generics, status
# from rest_framework.response import Response  # ✅ Required for returning JSON responses

# class AddressListCreateAPIView(generics.ListCreateAPIView):
#     queryset = address.objects.all()
#     serializer_class = addressSerializer
#     permission_classes = [AllowAny]  # No authentication required

#     def perform_create(self, serializer):
#         serializer.save()  # Removed user assignment

# class AddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = address.objects.all()
#     serializer_class = addressSerializer
#     permission_classes = [AllowAny]  # No authentication required

