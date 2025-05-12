from rest_framework import generics
from .models import SubscriptionPlan, SubscriptionBenefit
from .serializers import SubscriptionPlanSerializer, SubscriptionBenefitSerializer
from rest_framework.permissions import AllowAny

# Create Subscription Plan with benefits
class SubscriptionPlanCreateView(generics.CreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]  # Allow access without authentication

# List all Subscription Plans
class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.prefetch_related('benefits').all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]  # Allow access without authentication

# Get details of a single Subscription Plan
class SubscriptionPlanDetailView(generics.RetrieveAPIView):
    queryset = SubscriptionPlan.objects.prefetch_related('benefits').all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]  # Allow access without authentication
