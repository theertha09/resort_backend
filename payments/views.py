from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SubscriptionBenefit

import razorpay

from login.models import form  # Custom user model
from .models import SubscriptionPlan, Payment
from .serializers import SubscriptionPlanSerializer, PaymentSerializer# Ensure you have Razorpay credentials in your settings

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Create Subscription Plan with benefits
class SubscriptionPlanCreateView(generics.CreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]


# List all Subscription Plans
class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.prefetch_related('benefits').all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]


# Get details of a single Subscription Plan
class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.prefetch_related('benefits').all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    permission_classes = [AllowAny]# Payment ViewSet (CRUD if needed)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


# Create Razorpay Order APIView
class CreateOrderAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Step 1: Get user_uuid and subscription_plan_uuid from the request data
            user_uuid = request.data.get('user_uuid')
            subscription_plan_uuid = request.data.get('subscription_plan_uuid')

            if not user_uuid or not subscription_plan_uuid:
                return Response({'error': 'user_uuid and subscription_plan_uuid are required.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Retrieve the User (form) instance
            try:
                user = form.objects.get(uuid=user_uuid)
            except form.DoesNotExist:
                return Response({'error': 'User with this user_uuid not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Step 3: Retrieve the Subscription Plan instance
            try:
                subscription_plan = SubscriptionPlan.objects.get(uuid=subscription_plan_uuid)
            except SubscriptionPlan.DoesNotExist:
                return Response({'error': 'Subscription Plan with this subscription_plan_uuid not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Step 4: Use the base price directly without GST
            final_price = float(subscription_plan.amount)

            # Step 5: Create a payment record in the database
            payment = Payment.objects.create(
                user=user,
                subscription_plan=subscription_plan,
                amount=final_price,
                status='unpaid',
            )

            # Step 6: Create Razorpay order
            order_data = {
                'amount': int(final_price * 100),  # Razorpay expects amount in paise
                'currency': 'INR',
                'receipt': str(payment.id),
                'notes': {
                    'subscription_plan': str(subscription_plan.uuid),
                    'plan_type': subscription_plan.name
                }
            }

            razorpay_order = client.order.create(data=order_data)

            # Step 7: Save Razorpay order ID
            payment.razorpay_order_id = razorpay_order['id']
            payment.save()

            return Response({
                'order_id': razorpay_order['id'],
                'amount': final_price,
                'currency': 'INR',
                'payment_id': str(payment.id),
                'user_uuid': str(user.uuid),
                'plan_type': subscription_plan.name,
                'final_price': final_price,
                'payment_status': payment.status,
                'base_price': final_price
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Payment verification
# Verify Razorpay Payment
class VerifyPaymentAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Extract details from frontend
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_signature = request.data.get('razorpay_signature')

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response({'error': 'Missing required Razorpay parameters.'}, status=status.HTTP_400_BAD_REQUEST)

            # Find payment record by order_id
            try:
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            except Payment.DoesNotExist:
                return Response({'error': 'Payment record not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Step 1: Verify signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return Response({'error': 'Signature verification failed.'}, status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Mark payment as successful
            payment.razorpay_payment_id = razorpay_payment_id
            payment.status = 'paid'
            payment.save()

            return Response({'success': True, 'message': 'Payment verified and updated successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_all_payments(request):
    if request.method == "GET":
        payments = Payment.objects.all().order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return JsonResponse({"payments": serializer.data}, safe=False)
@api_view(['DELETE'])
@permission_classes([AllowAny])  # No auth required
def delete_benefit(request, subscription_uuid, benefit_id):
    try:
        # Verify the subscription exists
        subscription = SubscriptionPlan.objects.get(uuid=subscription_uuid)

        # Get the benefit under that subscription
        benefit = SubscriptionBenefit.objects.get(id=benefit_id, plan=subscription)
        benefit.delete()
        return Response({'message': 'Benefit deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except SubscriptionPlan.DoesNotExist:
        return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)

    except SubscriptionBenefit.DoesNotExist:
        return Response({'error': 'Benefit not found under this subscription'}, status=status.HTTP_404_NOT_FOUND)
