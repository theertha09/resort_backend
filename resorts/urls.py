"""
URL configuration for resorts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
# Swagger schema view setup with public access
schema_view = get_schema_view(
    openapi.Info(
        title="RESORT API",
        default_version='v1',
        description="API documentation for RESORT API",
        terms_of_service="https://www.yourproject.com/terms/",
        contact=openapi.Contact(email="anaghavm2019@gmail.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)








urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login.urls')),
    path('api/', include('phone.urls')),  # Include phone app URLs
    path('api/', include('product.urls')),  # Include phone app URLs
    path('api/', include('properties.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('points.urls')),
    path('api/', include('addresses.urls')),
    path('api/', include('coins.urls')),
    path('api/', include('form.urls')),  # Include form app URLs
   # Swagger documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
