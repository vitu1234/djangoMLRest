from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status,permissions


import json
from datetime import datetime
import pymongo
from bson.timestamp import Timestamp
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
    if(request_data_copy.get('device_type') is None):
        return Response({"error":True, "msg":"Device type not set"}, status=status.HTTP_400_BAD_REQUEST)
    if(request_data_copy.get('device_name') is None):
        return Response({"error":True, "msg":"Device Name not set"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request_data_copy.get('device_type') == 'sensor':
        if(request_data_copy.get('raw_readings_type') is None):
            return Response({"error":True, "msg":"Device readings type not set"}, status=status.HTTP_400_BAD_REQUEST)
        if(request_data_copy.get('raw_readings_units_type') is None):
            return Response({"error":True, "msg":"Device readings units type not set"}, status=status.HTTP_400_BAD_REQUEST)
     #check if device already exists
     #    
    database = ApiConfig.get_mongo_database()
    collection1 = database["user_devices"]
    cursor1 = collection1.find({ "device_id": request_data_copy.get('device_id') })

    if(cursor1.count()==0):
        serializer = UserDeviceSerializer(data=request_data_copy)
        if serializer.is_valid():
            serializer.save()
            #update the unclaimed devices records and set device type 
            #sensor has readings while actuators does not have readings
            
            collection = database["devices"]
            myquery = { "flotta_egdedevice_id": request_data_copy.get('device_id') }
            cursor = collection.find(myquery)
            if request_data_copy.get('device_type') == 'sensor':
                if cursor.count() > 0:
                    newvalues = { 
                    "$set": {
                            'user_claim':True,
                            'device_type': request_data_copy.get('device_type'),
                            'columns_readings_type':((request_data_copy.get('raw_readings_type').lower()).strip()).replace(" ", ""),
                            'columns_readings_units_type':(request_data_copy.get('raw_readings_units_type').strip()).replace(" ", "")
                            }
                    }
                    collection.update_one(myquery, newvalues)
                else:
                    newdevice = {
                            'user_claim':True,
                            'device_type': request_data_copy.get('device_type'),
                            'columns_readings_type':((request_data_copy.get('raw_readings_type').lower()).strip()).replace(" ", ""),
                            'columns_readings_units_type':(request_data_copy.get('raw_readings_units_type').strip()).replace(" ", "")
                            }
                    collection.insert_one(newdevice)
            else:
                if cursor.count() > 0:
                    newvalues = { 
                    "$set": {
                            'user_claim':True,
                            'device_type': request_data_copy.get('device_type')
                            }
                    }
                    collection.update_one(myquery, newvalues)
                else:
                    newdevice = {
                            'user_claim':True,
                            'device_type': request_data_copy.get('device_type')
                            }
                    collection.insert_one(newdevice)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": True, "msg":"Device has already been added"}, status=status.HTTP_400_BAD_REQUEST)

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
                    
                    collection3 = database["sensors"]
                    cursor3 = collection3.find_one({"flotta_egdedevice_id":document2['device_id']},sort=[( 'timestamp', pymongo.DESCENDING )])

                    collection4 = database["devices"]
                    cursor4 = collection4.find_one({"flotta_egdedevice_id":document2['device_id']})

                    date_time_str = str(cursor3['timestamp'])
                    date_time_obj =datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
                    date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                    row = {
                        "id": document2['id'],
                        "farm_id": document['id'],
                        "device_id": document2['device_id'],
                        "device_name": document2['device_name'],
                        "switch_status": document2['switch_status'],
                        "description": document2['description'],
                         "timestamp": date_time_str,

                        "user_id": document['user_id'],
                        "farm_name": document['farm_name'],
                        "address": document['address'],
                        "longtude": document['longtude'],
                        "latitude": document['latitude'],
                    }

                    raw_readings_type_list =  (((cursor4['columns_readings_type'].lower()).strip()).replace(" ", "")).split(",") #lower case,remove commas and spaces and covert to array
                    raw_readings_units_type_list =  (((cursor4['columns_readings_units_type'].lower()).strip()).replace(" ", "")).split(",") #lower case,remove commas and spaces and covert to array
                    i = 0
                    units={}
                    for value in raw_readings_type_list:
                        if value !="":
                            row[value]=cursor3[value]
                            if i <= len(raw_readings_units_type_list):
                                units[value]=raw_readings_units_type_list[i]
                        i+=1        
                            
                    row['units']=units
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