
from django.urls import path
from .views import pointsListCreateAPIView
urlpatterns = [
    path('points/', pointsListCreateAPIView.as_view(), name='points-list'),
]