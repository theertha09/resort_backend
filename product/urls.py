from django.urls import path
from .views import (
    StateListCreateAPIView, StateRetrieveUpdateDestroyAPIView,
    ResortListCreateAPIView, ResortRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # State APIs
    path('place/', StateListCreateAPIView.as_view(), name='state-list-create'),
    path('place/<int:id>/', StateRetrieveUpdateDestroyAPIView.as_view(), name='state-detail'),

    # Resort APIs
    path('resorts/', ResortListCreateAPIView.as_view(), name='resort-list-create'),
    path('resorts/<int:id>/', ResortRetrieveUpdateDestroyAPIView.as_view(), name='resort-detail'),
]
