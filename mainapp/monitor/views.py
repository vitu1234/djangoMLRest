from django.shortcuts import render

# Create your views here.
import numpy as np
import pandas as pd
from .apps import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json


class Prediction(APIView):
    def post(self, request):
        # data = request.data
        json_data = json.loads(request.body)

        temperature= json_data['temperature']
        humidity = json_data['humidity']
        soil_moisture = json_data['soil_moisture']
        
        dtree = ApiConfig.model
        #predict using independent variables
        PredictionMade = dtree.predict([[temperature, humidity, soil_moisture]])

        response_dict = {"Predicted values": PredictionMade}
        # print(response_dict)
        return Response(response_dict, status=200)