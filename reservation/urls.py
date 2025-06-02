from django.urls import path
from .views import ReservationCreateAPIView, ReservationDetailAPIView

urlpatterns = [
    path('reserve/', ReservationCreateAPIView.as_view(), name='reservation-create-list'),
    path('reserve/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
]
