
from django.urls import path
from authentication.views import RegisterAPIView 
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
]