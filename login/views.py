from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password,is_password_usable

from rest_framework.permissions import IsAuthenticated

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .models import form as Form  # Ideally rename model to Form
from .serializers import FormSerializer
from .serializers import ChangePasswordSerializer, SetInitialPasswordSerializer, ResetPasswordSerializer  # Import your serializer


GOOGLE_CLIENT_ID = "508003736604-vuhp0i91qrsbm81n4pmu93jrvjq71fr4.apps.googleusercontent.com"


# List and Create form entries
class FormListCreateAPIView(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [AllowAny]


# Retrieve, Update, Delete form entry by UUID
class FormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'uuid'
    permission_classes = [AllowAny]


# Google OAuth Login/Register
class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify token with Google
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
            email = idinfo['email']
            full_name = idinfo.get('name', 'No Name')

            user, created = Form.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': full_name,
                    'phone_number': '',
                    'password': make_password(None),  # unusable password
                    'gender': 'Other',  # or make it optional
                }
            )

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
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# Test page view
def google_page(request):
    forms = Form.objects.all()
    return render(request, 'google_test.html', {'forms': forms})


class ChangePasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            try:
                user = Form.objects.get(uuid=uuid)

                # Debugging
                print("user.password:", user.password)
                print("is usable:", is_password_usable(user.password))
                print("check_password result:", check_password(old_password, user.password))

                # Unusable password? (e.g., from Google login)
                if not is_password_usable(user.password):
                    return Response({'error': 'Password change not allowed. This account was created via Google login or has no usable password.'}, status=status.HTTP_400_BAD_REQUEST)

                # Check old password
                if not check_password(old_password, user.password):
                    return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

                # Save new hashed password
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

            except Form.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetInitialPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SetInitialPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            try:
                user = Form.objects.get(uuid=uuid)
                
                # Check if user already has a usable password
                if is_password_usable(user.password):
                    return Response({'error': 'User already has a password set.'}, status=status.HTTP_400_BAD_REQUEST)

                # Set new password
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Initial password set successfully.'}, status=status.HTTP_200_OK)

            except Form.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uuid = serializer.validated_data['uuid']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            try:
                user = Form.objects.get(uuid=uuid)
                
                # Set new password
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)

            except Form.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
