from django.urls import path
from .views import (
    FormListCreateAPIView,
    FormRetrieveUpdateDestroyAPIView,
    GoogleAuthView,
    google_page,
    ResetPasswordAPIView,LoginAPIView
)

urlpatterns = [
    path('', google_page, name='google-page'),
    path('register/', FormListCreateAPIView.as_view(), name='form-list-create'),
    path('register/<uuid:uuid>/', FormRetrieveUpdateDestroyAPIView.as_view(), name='form-detail'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('auth/google/', GoogleAuthView.as_view(), name='google-login'),
    path('login/', LoginAPIView.as_view(), name='login'),

]