from django.urls import path
from .views import SubscriptionPlanCreateView, SubscriptionPlanListView, SubscriptionPlanDetailView

urlpatterns = [
    path('subscription-plans/create/', SubscriptionPlanCreateView.as_view(), name='subscription-plan-create'),
    path('subscription-plans/', SubscriptionPlanListView.as_view(), name='subscription-plan-list'),
    path('subscription-plans/<uuid:id>/', SubscriptionPlanDetailView.as_view(), name='subscription-plan-detail'),
]
