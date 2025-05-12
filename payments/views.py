from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from django.conf import settings
import razorpay
from properties.models import FormData  # Ensure this import is at the top
import uuid
from .models import SubscriptionPlan, Payment
from .serializers import SubscriptionPlanSerializer, PaymentSerializer

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
            subscription_plan_id = request.data.get('subscription_plan')
            resort_id = request.data.get('resort')

            if not subscription_plan_id:
                return Response({'error': 'Subscription plan ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
            except SubscriptionPlan.DoesNotExist:
                return Response({'error': 'SubscriptionPlan not found.'}, status=status.HTTP_404_NOT_FOUND)

            resort = None
            if resort_id:
                try:
                    resort_uuid = uuid.UUID(resort_id)
                    resort = FormData.objects.get(id=resort_uuid)
                except (FormData.DoesNotExist, ValueError):
                    return Response({'error': 'Invalid resort UUID.'}, status=status.HTTP_400_BAD_REQUEST)

            # Use the base amount from the plan (no discount)
            base_price = float(subscription_plan.amount)

            # Calculate only GST
            gst_percentage = 18
            gst_amount = base_price * gst_percentage / 100
            final_price = round(base_price + gst_amount, 2)

            # Create payment record
            payment = Payment.objects.create(
                subscription_plan=subscription_plan,
                amount=final_price,
                resort=resort
            )

            # Create Razorpay order
            order_data = {
                'amount': int(final_price * 100),  # in paise
                'currency': 'INR',
                'receipt': str(payment.id),
                'notes': {
                    'subscription_plan': str(subscription_plan.id),
                    'plan_type': subscription_plan.name
                }
            }

            razorpay_order = client.order.create(data=order_data)
            payment.razorpay_order_id = razorpay_order['id']
            payment.save()

            return Response({
    'order_id': razorpay_order['id'],
    'amount': final_price,  # Return final price in rupees
    'currency': 'INR',
    'payment_id': str(payment.id),
    'plan_type': subscription_plan.name,
    'final_price': final_price,
    'gst_amount': gst_amount,
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
        except Exception as e:  # If signature verification fails
            return Response({'error': f"Payment signature verification failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        payment.razorpay_payment_id = params_dict['razorpay_payment_id']
        payment.razorpay_signature = params_dict['razorpay_signature']
        payment.status = 'completed'
        payment.save()

        return Response({'status': 'success'})

    except Exception as e:
        return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
