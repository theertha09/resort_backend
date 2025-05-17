from django.urls import path
from .views import FormListCreateAPIView, FormRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('forms/', FormListCreateAPIView.as_view(), name='form-list-create'),
    path('forms/<int:pk>/', FormRetrieveUpdateDestroyAPIView.as_view(), name='form-detail'),
]
