# points/urls.py

from django.urls import path
from .views import PointsListCreateAPIView, PointsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('points/', PointsListCreateAPIView.as_view(), name='points-list-create'),
    path('points/<uuid:uuid>/', PointsRetrieveUpdateDestroyAPIView.as_view(), name='points-detail'),
]
