from django.urls import path, include
from .views import *


urlpatterns = [

  path('api/devices/unclaimed', unclaimed_devices), #get unclaimed devices
  path('api/user/add_device', add_user_device), #add user device
  path('api/user/devices', user_devices), #get user devices
  path('api/user/farm/devices/<int:farm_id>', user_farm_devices), #get user devices

]