
from django.urls import path
from .views import PointsListCreateAPIView,PointsRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('points/', PointsListCreateAPIView.as_view(), name='points-list'),
    path('points/<int:pk>/', PointsRetrieveUpdateDestroyAPIView.as_view(), name='points-detail'),
]