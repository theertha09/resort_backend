from django.urls import path
from .views import (
    FormListCreateAPIView,
    FormRetrieveUpdateDestroyAPIView,GoogleAuthView,google_page
)

urlpatterns = [
    path('', google_page, name='google-page'),
    path('register/', FormListCreateAPIView.as_view(), name='form-list-create'),
    path('register/<uuid:uuid>/', FormRetrieveUpdateDestroyAPIView.as_view(), name='form-detail'),

    path('auth/google/', GoogleAuthView.as_view(), name='google-login'),

]