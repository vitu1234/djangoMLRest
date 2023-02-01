from django.db import DatabaseError
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
from .serializers import UserSerializer
from .serializers import MyTokenObtainPairSerializer

#paho mqtt
import random
import os
from paho.mqtt import client as mqtt_client
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )

ApiConfig = apps.ApiConfig

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
  
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# view for registering users
class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        request_data_copy = request.data.copy()

        #validate form fields and make user all fields are properly set
        if(request_data_copy.get('username') is None):
            return Response({"error":True, "msg":"Username not set"}, status=status.HTTP_400_BAD_REQUEST)
        if(request_data_copy.get('email') is None):
            return Response({"error":True, "msg":"Email not set"}, status=status.HTTP_400_BAD_REQUEST)
        if(request_data_copy.get('password') is None):
            return Response({"error":True, "msg":"Password not set"}, status=status.HTTP_400_BAD_REQUEST)
        if(request_data_copy.get('first_name') is None):
            return Response({"error":True, "msg":"First Name not set"}, status=status.HTTP_400_BAD_REQUEST)
        if(request_data_copy.get('last_name') is None):
            return Response({"error":True, "msg":"Last Name not set"}, status=status.HTTP_400_BAD_REQUEST)
        
        #check if user exists in the database
        database = ApiConfig.get_mongo_database()
    
        collection = database["user_user"]
        
        cursor2 = collection.find_one({"email":request_data_copy.get('email')}) 
        if cursor2 != None:
            return Response({"error":True, "msg":"Username or email in use"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=False)
        # serializer.save()
        # return Response(serializer.data)
        try:
            serializer.is_valid(raise_exception=False)
            serializer.save()
            results = serializer.data
            results['error'] =False
            return Response(results, status=status.HTTP_201_CREATED)
        except DatabaseError as e:
            return Response({"error":True, "msg":"An error occured on the server, if it persits, contact system admin!"},status=status.HTTP_400_BAD_REQUEST)

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







