from django.urls import path
from .views import create_referral,get_user_referrals,delete_user_referral,list_all_referrals

urlpatterns = [
    path('referrals/create/', create_referral, name='create-referral'),
    path('referrals/', get_user_referrals, name='get_user_referrals'),
    path('referrals/delete/', delete_user_referral, name='delete_user_referral'),
    path('referrals/all/', list_all_referrals, name='list-all-referrals'),  # ✅ New route


]
