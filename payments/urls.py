from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionPlanCreateView, SubscriptionPlanListView, SubscriptionPlanDetailView,
    PaymentViewSet, CreateOrderAPIView, verify_payment
)
from . import views  # 🔧 Import views for get_all_payments

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('subscription/create/', SubscriptionPlanCreateView.as_view(), name='subscription-create'),
    path('subscription/list/', SubscriptionPlanListView.as_view(), name='subscription-list'),
    path('subscription/<uuid:id>/', SubscriptionPlanDetailView.as_view(), name='subscription-detail'),
    path('create-order/', CreateOrderAPIView.as_view(), name='create-order'),
    path('verify-payment/', verify_payment, name='verify-payment'),
    path('payments/', views.get_all_payments, name='getall-payments'),  # ✅ Fixed

    path('', include(router.urls)),
]
