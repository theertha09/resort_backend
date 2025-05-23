from django.urls import path
from .views import (
    StateListCreateAPIView, StateRetrieveUpdateDestroyAPIView,
    ResortListCreateAPIView, ResortRetrieveUpdateDestroyAPIView,PropertyListCreateView,PropertyRetrieveUpdateDestroyView,FeatureListCreateView,FeatureRetrieveUpdateDestroyView
)

urlpatterns = [
    # State APIs
    path('place/', StateListCreateAPIView.as_view(), name='state-list-create'),
    path('place/<int:id>/', StateRetrieveUpdateDestroyAPIView.as_view(), name='state-detail'),

    # Resort APIs
    path('resorts/', ResortListCreateAPIView.as_view(), name='resort-list-create'),
    path('resorts/<int:id>/', ResortRetrieveUpdateDestroyAPIView.as_view(), name='resort-detail'),

    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),
    path('feactures/', FeatureListCreateView.as_view(), name='feactures-list-create'),
    path('feactures/<int:pk>/', FeatureRetrieveUpdateDestroyView.as_view(), name='feactures-detail'),

]
