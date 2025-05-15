from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from django.conf import settings
from login.models import form  # Assuming the form model is in the login app
import razorpay
import uuid
from .models import SubscriptionPlan, Payment
from .serializers import SubscriptionPlanSerializer, PaymentSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Ensure you have Razorpay credentials in your settings

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
class SubscriptionPlanDetailView(generics.RetrieveAPIView):
    queryset = SubscriptionPlan.objects.prefetch_related('benefits').all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]


# Payment ViewSet (CRUD if needed)
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
                subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_uuid)
            except SubscriptionPlan.DoesNotExist:
                return Response({'error': 'Subscription Plan with this subscription_plan_uuid not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Step 4: Calculate the final price including GST
            base_price = float(subscription_plan.amount)
            gst_percentage = 18
            gst_amount = base_price * gst_percentage / 100
            final_price = round(base_price + gst_amount, 2)

            # Step 5: Create a payment record in the database
            payment = Payment.objects.create(
                user=user,
                subscription_plan=subscription_plan,
                amount=final_price,
                status='completed',  # Set to 'completed' initially
            )

            # Step 6: Create Razorpay order
            order_data = {
                'amount': int(final_price * 100),  # Razorpay expects amount in paise
                'currency': 'INR',
                'receipt': str(payment.id),
                'notes': {
                    'subscription_plan': str(subscription_plan.id),
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
                'gst_amount': gst_amount,
                'payment_status': payment.status,
                'base_price': base_price
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Payment verification
@api_view(['POST'])
def verify_payment(request):
    try:
        payment = Payment.objects.get(id=request.data.get('payment_id'))

        params_dict = {
            'razorpay_order_id': request.data.get('razorpay_order_id'),
            'razorpay_payment_id': request.data.get('razorpay_payment_id'),
            'razorpay_signature': request.data.get('razorpay_signature')
        }

        # Verify payment signature
        try:
            client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            return Response(
                {'error': f"Payment signature verification failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update payment status if verification passes
        payment.razorpay_payment_id = params_dict['razorpay_payment_id']
        payment.razorpay_signature = params_dict['razorpay_signature']
        payment.status = 'completed'
        payment.save()

        return Response({'status': 'success'})

    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def get_all_payments(request):
    if request.method == "GET":
        payments = Payment.objects.all().order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return JsonResponse({"payments": serializer.data}, safe=False)
