from django.urls import path
from .views import ( GenerateAccessTokenAPIView, LogInUserNameAPIView, 
        UserDetails ,
        RegisterAPIView ,
        SendEmailVerficationAPIView , VerifyEmailOrEmailActivationAPIView,
        )

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
    
    path('login/' ,LogInUserNameAPIView.as_view()) ,
   
    # generate access token using refresh token
    path('generate_access_token/' ,GenerateAccessTokenAPIView.as_view()),

    # to verify your email and match the OTP code.
    path('EmailOTPpVerfication/' ,VerifyEmailOrEmailActivationAPIView.as_view())

    
]
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjc0ODk2Njg1fQ.5lXmRTZ-xXLK_yCIxS1nTpscBOtRcYW5894RwyTHkMA