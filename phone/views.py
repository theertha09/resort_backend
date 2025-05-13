from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PhoneNumber
import firebase_admin
from firebase_admin import credentials, auth

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('resortbackend-firebase-adminsdk-fbsvc-36a86138da.json')  # Replace with your Firebase Admin SDK key
    firebase_admin.initialize_app(cred)

@api_view(['POST'])
def register_phone_number(request):
    phone_number = request.data.get('phone_number')

    if phone_number:
        try:
            # Create or update Firebase user
            user_record = auth.create_user(phone_number=phone_number)
            uid = user_record.uid  # Extract the UID from the UserRecord

            # Save the phone number to the database
            phone_entry = PhoneNumber.objects.create(phone_number=phone_number)
            
            return Response({"message": "Phone number registered successfully.", "uid": uid}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_phone_number(request, uid):
    """
    Deletes a phone number from the database and Firebase.
    """
    try:
        # Delete the user from Firebase using the UID
        auth.delete_user(uid)

        # Delete the phone number from the database
        phone_entry = get_object_or_404(PhoneNumber, phone_number=request.data.get('phone_number'))
        phone_entry.delete()

        return Response({"message": "Phone number deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
