from django.urls import path
from .views import AddressListCreateView, AddressDetailView

urlpatterns = [
    path('address/', AddressListCreateView.as_view(), name='address-list-create'),
    path('address/<int:id>/', AddressDetailView.as_view(), name='address-detail'),  # 🔍 MUST use <int:id>
]
