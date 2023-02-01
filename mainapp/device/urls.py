from django.urls import path, include
from .views import *


urlpatterns = [

  path('api/devices/unclaimed', unclaimed_devices), #get unclaimed devices
  path('api/user/add_device', add_user_device),


]