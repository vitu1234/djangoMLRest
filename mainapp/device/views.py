from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status,permissions


import json
from monitor import apps
from .models import UserDevice 
from .serializers import UserDeviceSerializer

ApiConfig = apps.ApiConfig


#get unclaimed devices
@api_view(['GET'])
@permission_classes((AllowAny, ))
def unclaimed_devices(request):
    database = ApiConfig.get_mongo_database()
    
    collection = database["devices"]
    cursor = collection.find({"user_claim":False})

    devices_unclaimed = [] 
    if cursor != None:
        for document in cursor:

            row = {
                "flotta_egdedevice_id": document['flotta_egdedevice_id'],
                "user_claim": document['user_claim'],
                "mode": document['mode']
            }
            devices_unclaimed.append(row)
        data_array = {
            "error":False, 
            "msg":"Unclaimed devices",
            "unclaimed_devices": devices_unclaimed
        }
        
        return Response(data_array, status=200)
    else:
        return Response({"error": True, "msg":"No Unclaimed devices"}, status=200)

# add user device to a farm already added in db
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_user_device(request):
    request_data_copy = request.data.copy()

    #validate form fields and make all fields are properly set
    if(request_data_copy.get('farm_id') is None):
        return Response({"error":True, "msg":"Farm name not set"}, status=status.HTTP_400_BAD_REQUEST)
    if(request_data_copy.get('device_id') is None):
        return Response({"error":True, "msg":"Device ID not set"}, status=status.HTTP_400_BAD_REQUEST)
    if(request_data_copy.get('device_name') is None):
        return Response({"error":True, "msg":"Device Name not set"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserDeviceSerializer(data=request_data_copy)
    if serializer.is_valid():
        serializer.save()
        #update the unclaimed devices records
        database = ApiConfig.get_mongo_database()
        collection = database["devices"]
        myquery = { "flotta_egdedevice_id": request_data_copy.get('device_id') }
        newvalues = { "$set": {"user_claim":True} }
        collection.update_one(myquery, newvalues)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)