from django.urls import path, include
from .views import *


urlpatterns = [

  path('api/user/farms', user_farms), #get user farms
  path('api/user/add_farm', add_user_farm), #add user farm
  path('api/user/register_farm', register_user_farm), #register user farm

]