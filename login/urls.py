from django.urls import path
from .views import (
    FormListCreateAPIView,
    FormRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('register/', FormListCreateAPIView.as_view(), name='form-list-create'),
    path('register/<uuid:uuid>/', FormRetrieveUpdateDestroyAPIView.as_view(), name='form-detail'),
]