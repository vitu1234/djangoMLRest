from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
import numpy as np
import pandas as pd
from .apps import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from monitor import apps

#influxdb
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from pandas import DataFrame
import json
from datetime import datetime
import pymongo

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status, permissions
from .serializers import UserSerializer,RegisterSerializer

#paho mqtt
import random
import os
from paho.mqtt import client as mqtt_client
ApiConfig = apps.ApiConfig

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


#get device predicitions
@api_view(['GET'])
def prediction_by_device(request, flotta_device_id):
    database = ApiConfig.get_mongo_database()
    
    collection = database["sensors"]
    device = flotta_device_id
    #get data based on device_id
    cursor2 = collection.find_one({"flotta_egdedevice_id":device},sort=[( 'timestamp', pymongo.DESCENDING )]) 
    if cursor2 != None:

        PredictionMade = ApiConfig.get_prediction(cursor2['temperature'], cursor2['humidity'],cursor2['soil_moisture'])
        
        data = {
            "error": False,
            "flotta_egdedevice_id": device,
            "temperature": cursor2['temperature'],
            "humidity": cursor2['humidity'],
            "actual_soil_moisture": cursor2['soil_moisture'],
            "predicted_soil_moisture": float(format(float(PredictionMade), '.2f'))
        }
        return Response(data, status=200)
    else:
        return Response({"error": True}, status=200)

@api_view(['POST'])
def create_user_account(request):
    data = json.loads(request.body)
    
    username = data['username']
    email = data['password']
    password = data['password']

    client = ApiConfig.connect_mqtt()
    client.loop_start()
    result = ApiConfig.publish_mqtt(client, data['pump_device_id'], data['pump_action'])
    if(result):
        return Response({"published": True }, status=200)
    else:
        return Response({"published": False }, status=200)

#register user
@api_view(['POST'])
def register(request, format='json'):
    permission_classes = (AllowAny,)
    request_data_copy = request.data.copy()
    user_serializer = UserSerializer(data=request_data_copy)
    user_serializer.is_valid()
    user = user_serializer.save()

    if user:
        user_json = user_serializer.data
        return Response(user_json, status=status.HTTP_201_CREATED)
    else:
        return Response({"failed":True}, status=status.HTTP_417_EXPECTATION_FAILED)








