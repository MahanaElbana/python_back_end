from django.urls import path
from .views import ( UserDetails ,
         RegisterAPIView ,
          SendEmailVerficationAPIView , LogInAPIView)

from rest_framework.authtoken import views
'''--------------------------------------------'''
'''from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)'''

app_name = 'auth_user_app'
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

    ## ------------- api/auth --------------------------###
    path('user/', UserDetails.as_view(), name='user'),
    path('register/', RegisterAPIView.as_view()) ,
    path('SendEmailVerfication/' ,SendEmailVerficationAPIView.as_view()) ,
    
    path('login/' ,LogInAPIView.as_view()) ,
  
    
]