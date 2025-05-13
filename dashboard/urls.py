# address/urls.py
from django.urls import path
from .views import (
    AddressListCreateAPIView,
    AddressRetrieveUpdateDestroyAPIView,
    BulkListCreateAPIView
)

urlpatterns = [
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyAPIView.as_view(), name='address-detail'),
    path('referrals/bulk/', BulkListCreateAPIView.as_view(), name='bulk-referral-create'),
    # path('referrals/user/<uuid:uuid>/', ReferralListByUserUUIDAPIView.as_view(), name='referral-by-user'),

]
