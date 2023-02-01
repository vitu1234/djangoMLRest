from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status,permissions
from rest_framework.decorators import api_view, permission_classes

from .serializers import (FarmSerializer)
from monitor import apps
from user import models as UserModel
from user import serializers as UserSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
ApiConfig = apps.ApiConfig
User = UserModel.User
UserSerializer = UserSerializers.UserSerializer

#get user farms
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_farms(request):

    #get logged in user
    serializer = UserSerializer(request.user)
    logged_user = serializer.data
    # return Response(logged_user["id"])

    database = ApiConfig.get_mongo_database()
    
    collection = database["user_farms"]
    cursor = collection.find({"user_id": logged_user["id"]})
    results = list(cursor)

    user_farms = [] 
    if len(results) >0:
        for document in cursor:

            row = {
                "flotta_egdedevice_id": document['flotta_egdedevice_id'],
                "user_claim": document['user_claim'],
                "mode": document['mode']
            }
            user_farms.append(row)
        data_array = {
            "error":False, 
            "msg":"Unclaimed devices",
            "unclaimed_devices": user_farms
        }
        
        return Response(data_array, status=status.HTTP_200_OK)
    else:
        return Response({"error": True, "msg":"No user farms"}, status=status.HTTP_200_OK)


#add user farms
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_user_farm(request):
    #get logged in user
    serializer = UserSerializer(request.user)
    logged_user = serializer.data
    request_data_copy = request.data.copy()

    #validate form fields and make user all fields are properly set
    if(request_data_copy.get('farm_name') is None):
        return Response({"error":True, "msg":"Farm name not set"}, status=status.HTTP_400_BAD_REQUEST)
    
    request_data_copy["user_id"]=logged_user["id"]
    serializer = FarmSerializer(data=request_data_copy)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
