from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404,render
from .models import form
from .serializers import FormSerializer 
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import form
from .serializers import FormSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from .models import form
import random
from rest_framework.views import APIView
from rest_framework.response import Response

GOOGLE_CLIENT_ID = "508003736604-vuhp0i91qrsbm81n4pmu93jrvjq71fr4.apps.googleusercontent.com"

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


class GoogleAuthView(APIView):
    permission_classes = []  # no login needed

    def post(self, request):
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'No token provided'}, status=400)

        try:
            # Verify with Google
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

            email = idinfo['email']
            full_name = idinfo.get('name', 'No Name')

            # Check if user exists
            user, created = form.objects.get_or_create(email=email, defaults={
                'full_name': full_name,
                'phone_number': '',  # optional
                'password': 'google-auth',  # dummy password
                'gender': 'Male',  # default or logic
            })

            # Create token
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'uuid': user.uuid,
                    'full_name': user.full_name,
                    'email': user.email,
                }
            })

        except ValueError:
            return Response({'error': 'Invalid token'}, status=400)

class GoogleAuthView(APIView):
    permission_classes = []  # no login needed

    def post(self, request):
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'No token provided'}, status=400)

        try:
            # Verify with Google
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

            email = idinfo['email']
            full_name = idinfo.get('name', 'No Name')

            # Check if user exists
            user, created = form.objects.get_or_create(email=email, defaults={
                'full_name': full_name,
                'phone_number': '',  # optional
                'password': 'google-auth',  # dummy password
                'gender': 'Male',  # default or logic
            })

            # Create token
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'uuid': user.uuid,
                    'full_name': user.full_name,
                    'email': user.email,
                }
            })

        except ValueError:
            return Response({'error': 'Invalid token'}, status=400)

def google_page(request):
    forms = form.objects.all()
    return render(request, 'google_test.html', {'forms': forms})