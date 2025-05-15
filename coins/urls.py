from django.urls import path
from .views import create_referral

urlpatterns = [
    path('referrals/create/', create_referral, name='create-referral'),
]
