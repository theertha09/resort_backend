from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
import razorpay
from rest_framework.decorators import api_view

from django.conf import settings
import hmac
import hashlib

from .models import FormData, FormDataImages,WelcomeSection,whychoose, Payment, SubscriptionPlan
from .serializers import FormDataSerializer, FormDataImagesSerializer,WelcomeSectionSerializer,whychooseSerializer,FormDataDetailSerializer, PaymentSerializer

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

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class PaymentViewSet(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Get the subscription plan
            subscription_plan = SubscriptionPlan.objects.get(id=request.data.get('subscription_plan'))
            
            # Create payment record
            payment_data = {
                'user_uuid': request.data.get('user_uuid'),
                'resort_uuid': request.data.get('resort_uuid'),
                'subscription_plan': subscription_plan,
                'amount': subscription_plan.offer_price
            }
            
            payment = Payment.objects.create(**payment_data)
            
            # Create Razorpay order
            order_data = {
                'amount': int(float(subscription_plan.offer_price) * 100),  # Convert to paise
                'currency': 'INR',
                'receipt': str(payment.id),
                'notes': {
                    'user_uuid': str(payment.user_uuid),
                    'resort_uuid': str(payment.resort_uuid),
                    'subscription_plan': str(payment.subscription_plan.id)
                }
            }
            
            razorpay_order = client.order.create(data=order_data)
            
            # Update payment with Razorpay order ID
            payment.razorpay_order_id = razorpay_order['id']
            payment.save()
            
            return Response({
                'order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency'],
                'payment_id': str(payment.id)
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_payment(request):
    try:
        # Get payment details
        payment = Payment.objects.get(id=request.data.get('payment_id'))
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': request.data.get('razorpay_order_id'),
            'razorpay_payment_id': request.data.get('razorpay_payment_id'),
            'razorpay_signature': request.data.get('razorpay_signature')
        }
        
        client.utility.verify_payment_signature(params_dict)
        
        # Update payment status
        payment.razorpay_payment_id = params_dict['razorpay_payment_id']
        payment.razorpay_signature = params_dict['razorpay_signature']
        payment.status = 'completed'
        payment.save()
        
        return Response({'status': 'success'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
