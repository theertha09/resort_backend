from django.urls import path
from .views import (
    FormDataListCreateAPIView,
    FormDataRetrieveUpdateDestroyAPIView,welcometaListCreateAPIView,welcomeRetrieveUpdateDestroyAPIView,FormDataFullDetailAPIView,whychooseRetrieveUpdateDestroyAPIView,whychooseListCreateAPIView,
    UploadMultipleImagesAPIView,
)

urlpatterns = [
    path('form-data/', FormDataListCreateAPIView.as_view(), name='form-data-list-create'),
    path('form-data/<uuid:id>/', FormDataRetrieveUpdateDestroyAPIView.as_view(), name='form-data-retrieve-update-destroy'),
    path('form-data/<uuid:id>/upload-multiple-images/', UploadMultipleImagesAPIView.as_view(), name='upload-multiple-images'),
    path('welcome/', welcometaListCreateAPIView.as_view(), name='form-data-list-create'),
    path('welcome/int:id>/', welcomeRetrieveUpdateDestroyAPIView.as_view(), name='form-data-retrieve-update-destroy'),
    path('whychoose/', whychooseListCreateAPIView.as_view(), name='form-data-list-create'),
    path('whychoose/int:id>/', whychooseRetrieveUpdateDestroyAPIView.as_view(), name='form-data-retrieve-update-destroy'),
    path('form-data/<uuid:id>/details/', FormDataFullDetailAPIView.as_view(), name='form-data-full-details'),

]
