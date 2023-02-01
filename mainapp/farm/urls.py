from django.urls import path, include
from .views import *


urlpatterns = [

  path('api/user/farms', user_farms), #get user farms
#   path('query_mongodb', query_mongodb),


]