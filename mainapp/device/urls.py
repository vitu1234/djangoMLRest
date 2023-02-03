from django.urls import path, include
from .views import *


urlpatterns = [

  #access unauthorized
  path('api/devices/unclaimed', unclaimed_devices), #get unclaimed devices
  path('api/devices/device/<str:flotta_egdedevice_id>', device_details), #get device details
  path('api/devices/register/<str:flotta_egdedevice_id>/<str:device_type>', register_device), #add device

  #access only authorized
  path('api/user/add_device', add_user_device), #add user device
  path('api/user/devices', user_devices), #get user devices
  path('api/user/farm/devices/<int:farm_id>', user_farm_devices), #get user devices

]