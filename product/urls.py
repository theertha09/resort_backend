from django.urls import path
from .views import (
    StateListCreateAPIView, StateRetrieveUpdateDestroyAPIView,
    ResortListCreateAPIView, ResortRetrieveUpdateDestroyAPIView,PropertyListCreateView,PropertyRetrieveUpdateDestroyView,FeatureListCreateView,FeatureRetrieveUpdateDestroyView,ResortFeaturePropertyRemoveAPIView
)

urlpatterns = [
    # State APIs
    path('place/', StateListCreateAPIView.as_view(), name='state-list-create'),
    path('place/<int:id>/', StateRetrieveUpdateDestroyAPIView.as_view(), name='state-detail'),

    # Resort APIs
    path('resorts/', ResortListCreateAPIView.as_view(), name='resort-list-create'),
    path('resorts/<int:id>/', ResortRetrieveUpdateDestroyAPIView.as_view(), name='resort-detail'),
    path('resorts/<int:resort_id>/remove-items/', ResortFeaturePropertyRemoveAPIView.as_view(), name='resort-remove-items'),

    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),
    path('features/', FeatureListCreateView.as_view(), name='feactures-list-create'),
    path('features/<int:pk>/', FeatureRetrieveUpdateDestroyView.as_view(), name='feactures-detail'),

]
