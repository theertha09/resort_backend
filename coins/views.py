from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Referral
from .serializers import ReferralSerializer
from payments.models import Payment  # ✅ Correct app and model name

@api_view(['POST'])
@authentication_classes([])  # Disable authentication
@permission_classes([])      # Disable permission checks
def create_referral(request):
    user_id = request.data.get('user_uuid')

    if not user_id:
        return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.filter(user__uuid=user_id, status='completed').latest('created_at')
        user = payment.user
        plan = payment.subscription_plan
    except Payment.DoesNotExist:
        return Response({'error': 'User has not completed any payment.'}, status=status.HTTP_403_FORBIDDEN)

    current_referrals = Referral.objects.filter(user=user).count()
    if plan.name.lower() == 'gold' and current_referrals >= 10:
        return Response({'error': 'Gold plan allows only 10 referrals.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ReferralSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])  # Disable authentication (you can add it later)
@permission_classes([])      # Disable permissions
def get_user_referrals(request):
    user_uuid = request.query_params.get('user_uuid')

    if not user_uuid:
        return Response({'error': 'user_uuid is required.'}, status=status.HTTP_400_BAD_REQUEST)

    referrals = Referral.objects.filter(user__uuid=user_uuid)
    serializer = ReferralSerializer(referrals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([])  # You can enable authentication later
@permission_classes([])
def delete_user_referral(request):
    user_uuid = request.query_params.get('user_uuid')
    referral_id = request.query_params.get('referral_id')

    if not user_uuid or not referral_id:
        return Response({'error': 'user_uuid and referral_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        referral = Referral.objects.get(id=referral_id, user__uuid=user_uuid)
    except Referral.DoesNotExist:
        return Response({'error': 'Referral not found or unauthorized.'}, status=status.HTTP_404_NOT_FOUND)

    referral.delete()
    return Response({'success': 'Referral deleted.'}, status=status.HTTP_200_OK)
