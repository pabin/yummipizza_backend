from django.urls import path, include
from .views import *


urlpatterns = [
    path('authentication/', UserAuthenticationAPIView.as_view(), name='user_authentication'),
    path('user/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user_read_update'),
    path('signup/', UserCreateAPIView.as_view(), name='user_signup'),
]
