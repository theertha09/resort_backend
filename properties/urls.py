from django.urls import path
from .views import (
    FormDataListCreateAPIView,
    FormDataRetrieveUpdateDestroyAPIView,
    welcometaListCreateAPIView,
    welcomeRetrieveUpdateDestroyAPIView,
    FormDataFullDetailAPIView,
    whychooseRetrieveUpdateDestroyAPIView,
    whychooseListCreateAPIView,
    UploadMultipleImagesAPIView,

    
)

urlpatterns = [
    path('form-data/', FormDataListCreateAPIView.as_view(), name='formdata-list-create'),
    path('form-data/<uuid:id>/', FormDataRetrieveUpdateDestroyAPIView.as_view(), name='formdata-retrieve-update-destroy'),
    path('form-data/<uuid:id>/upload-multiple-images/', UploadMultipleImagesAPIView.as_view(), name='formdata-upload-multiple-images'),
    path('welcome/', welcometaListCreateAPIView.as_view(), name='welcome-list-create'),
    path('welcome/<int:id>/', welcomeRetrieveUpdateDestroyAPIView.as_view(), name='welcome-retrieve-update-destroy'),
    path('whychoose/', whychooseListCreateAPIView.as_view(), name='whychoose-list-create'),
    path('whychoose/<int:id>/', whychooseRetrieveUpdateDestroyAPIView.as_view(), name='whychoose-retrieve-update-destroy'),
    path('form-data/<uuid:id>/details/', FormDataFullDetailAPIView.as_view(), name='formdata-full-details'),
]
