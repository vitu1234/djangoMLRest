from django.urls import path
from .views import *

urlpatterns = [
    path('prediction_by_device/<str:flotta_device_id>', prediction_by_device), #GET PREDICTIONS FROM THE ML MODEL
    path('create_user_account', create_user_account), #user register account
    path("get-details",UserDetailAPI.as_view()),
    path('register', register)
]