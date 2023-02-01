from django.urls import path, include
from .views import *


urlpatterns = [

  path('api/devices/unclaimed', unclaimed_devices), #get unclaimed devices
#   path('query_mongodb', query_mongodb),


]