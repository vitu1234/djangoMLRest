from django.urls import path
from .views import *

urlpatterns = [
    path('', Prediction.as_view(), name = 'prediction'),
    path('query_influxdb', QueryInfluxDB.as_view(), name = 'query_influxdb'),
    # path('query_mongodb', QueryMongoDB.as_view(), name = 'query_mongodb'),
    path('prediction_by_device/<str:flotta_device_id>', prediction_by_device), #GET PREDICTIONS FROM THE ML MODEL
    path('api/switch_by_device', action_to_device), #parameter is 0 or 1, 1=TURN ON and 0=TURN OFF 
    path('query_mongodb', query_mongodb),
]