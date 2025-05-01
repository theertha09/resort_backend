from django.urls import path
from .views import register_phone_number,delete_phone_number

urlpatterns = [
    path('phone-number/', register_phone_number, name='register-phone-number'),
    path('delete-number/<str:uid>/', delete_phone_number, name='delete-phone-number'),

]
