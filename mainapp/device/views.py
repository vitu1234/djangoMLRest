from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json
from monitor import apps
ApiConfig = apps.ApiConfig
# Create your views here.


#get unclaimed devices
@api_view(['GET'])
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

@api_view(['POST'])
def add_user_device(request):
    print("d")