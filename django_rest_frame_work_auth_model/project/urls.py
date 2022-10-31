"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path , include

''' -- drf-yasg - Yet another Swagger generator --'''
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

''' -- drf-yasg - Yet another Swagger generator --'''
schema_view = get_schema_view(
   openapi.Info(
      title="User API docs",
      default_version = 'v1',
      description="User model authentication and authorization ",
      contact=openapi.Contact(email="mahneyelbana@gmail.com"),
   ),
   public = True,
   permission_classes = [permissions.AllowAny],
   authentication_classes= [] ,
   
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User API [Login - send email verification - register ]
    path('api/auth/' ,include('auth_user_app.urls') , name= "User API") ,

    # ''' -- drf-yasg - Yet another Swagger generator --'''
    # path('swagger(?P<format>\.json|\.yaml)', 
    #   schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.json',schema_view.without_ui(cache_timeout=0), name='schema-json') ,  
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]









