from django.urls import path
from .views import PropertyRegistrationView,ContentListCreateAPIView,ContentDetailAPIView

urlpatterns = [
    path('content/', ContentListCreateAPIView.as_view(), name='content-list-create'),
    path('content/<int:pk>/', ContentDetailAPIView.as_view(), name='content-detail'),

    path('becomepartner/', PropertyRegistrationView.as_view(), name='property-register'),
]
