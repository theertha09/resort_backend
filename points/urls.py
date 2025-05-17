
from django.urls import path
from .views import pointsListCreateAPIView,pointsRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('points/', pointsListCreateAPIView.as_view(), name='points-list'),
    path('points/<int:id>/', pointsRetrieveUpdateDestroyAPIView.as_view(), name='points-detail'),
]