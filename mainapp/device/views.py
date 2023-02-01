from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status,permissions


import json
from monitor import apps
from device import models as DeviceModel 
from .serializers import UserDeviceSerializer
from user import models as UserModel
from user import serializers as UserSerializers

User = UserModel.User
UserSerializer = UserSerializers.UserSerializer

ApiConfig = apps.ApiConfig


#get unclaimed devices
@api_view(['GET'])
@permission_classes((AllowAny, ))
def unclaimed_devices(request):
    database = ApiConfig.get_mongo_database()
    
    collection = database["devices"]
    cursor = collection.find({"user_claim":False})

    devices_unclaimed = [] 
    if cursor.count() >0:
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

#get user devices
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_devices(request):

    #get logged in user
    serializer = UserSerializer(request.user)
    logged_user = serializer.data
    # return Response(logged_user["id"])

    database = ApiConfig.get_mongo_database()
    
    collection = database["user_farms"]
    cursor = collection.find({"user_id": logged_user["id"]})
    
    user_devices = [] 
    if cursor.count() >0: #make sure cursor is not empty
        for document in cursor:
            farm_id = document['id']
            
            collection2 = database["user_devices"]
            cursor2 = collection2.find({"farm_id": farm_id})
            if cursor2.count() >0:
                for document2 in cursor2:
                    row = {
                        "id": document2['id'],
                        "farm_id": document['id'],
                        "device_id": document2['device_id'],
                        "device_name": document2['device_name'],
                        "switch_status": document2['switch_status'],
                        "description": document2['description'],

                        "user_id": document['user_id'],
                        "farm_name": document['farm_name'],
                        "address": document['address'],
                        "longtude": document['longtude'],
                        "latitude": document['latitude'],
                    }
                    user_devices.append(row)
        data_array = {
            "error":False, 
            "msg":"User devices",
            "user_devices": user_devices
        }
        
        return Response(data_array, status=status.HTTP_200_OK)
    else:
        return Response({"error": True, "msg":"No user devices"}, status=status.HTTP_200_OK)

#get user farm devices
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_farm_devices(request, farm_id):
    database = ApiConfig.get_mongo_database()
    collection2 = database["user_devices"]
    cursor2 = collection2.find({"farm_id": farm_id})
    user_devices =[]
    if cursor2.count() >0:
        for document2 in cursor2:
            row = {
                "id": document2['id'],
                "farm_id": document2['farm_id'],
                "device_id": document2['device_id'],
                "device_name": document2['device_name'],
                "switch_status": document2['switch_status'],
                "description": document2['description'],
            }
            user_devices.append(row)
        data_array = {
            "error":False, 
            "msg":"Devices in farm",
            "user_devices": user_devices
        }
        
        return Response(data_array, status=status.HTTP_200_OK)
    else:
        return Response({"error": True, "msg":"No devices in farm"}, status=status.HTTP_200_OK)