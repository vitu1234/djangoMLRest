from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )
from .views import RegisterView


urlpatterns = [
    #apps
    path('prediction_by_device/<str:flotta_device_id>', prediction_by_device), #GET PREDICTIONS FROM THE ML MODEL
    path('create_user_account', create_user_account), #user register account
    path("get-details",UserDetailAPI.as_view()),
    path('register', register),

    #auth
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),


]