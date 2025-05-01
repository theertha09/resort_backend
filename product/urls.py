# resorts/urls.py

from django.urls import path
from .views import StateListAPIView, ResortListAPIView, ResortDetailAPIView

urlpatterns = [
    path('states/', StateListAPIView.as_view(), name='state-list'),
    path('resorts/', ResortListAPIView.as_view(), name='resort-list'),
    path('resorts/<uuid:id>/', ResortDetailAPIView.as_view(), name='resort-detail'),
]
