from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
import numpy as np
import pandas as pd
from .apps import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json

#influxdb
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from pandas import DataFrame
import json
from datetime import datetime
import pymongo

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
    
class Prediction(APIView):
    def post(self, request):
        # data = request.data
        json_data = json.loads(request.body)

        temperature= json_data['temperature']
        humidity = json_data['humidity']
        soil_moisture = json_data['soil_moisture']
        
        dtree = ApiConfig.model
        #predict using independent variables
        PredictionMade = ApiConfig.get_prediction(temperature, humidity,soil_moisture)

        response_dict = {"Predicted values": PredictionMade}
        # print(response_dict)
        return Response(response_dict, status=200)

class QueryInfluxDB(APIView):
    def get(self, request):
        # data = request.data
        # json_data = json.loads(request.body)

        # temperature= json_data['temperature']
        
        bucket = ApiConfig.BUCKET
        org = ApiConfig.ORG
        token = ApiConfig.TOKEN
        url=ApiConfig.URL
        client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )
        query_api = client.query_api()
        query = 'from(bucket: "mqtt_bucket")\
            |> range(start: -10m)\
            |> group(columns: ["flotta_egdedevice_id"]) \
            |> yield(name: "last")'
        q = 'import "influxdata/influxdb/schema"\n\nschema.measurements(bucket: "mqtt_bucket")'

        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record))
                # print(record.get_value())
        print(results)

        # print(response_dict)
        return Response({"dd": "results"}, status=200)


class QueryMongoDB(APIView):
    def get():
        # data = request.data
        # json_data = json.loads(request.body)

        # temperature= json_data['temperature']
        
        database = ApiConfig.get_mongo_database()
    
        collection = database["sensors"]
        data_array = []
        cursor = collection.distinct("flotta_egdedevice_id")
        for document in cursor:
            # date_time_str = str(document['timestamp'])
            # date_time_obj =datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
            # date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
            
            # row = {
            #     "flotta_egdedevice_id": document['flotta_egdedevice_id'],
            #     "temperature": document['temperature'],
            #     "humidity": document['humidity'],
            #     "soil_moisture": document['soil_moisture'],
            #     "timestamp": date_time_str
            # }
            # data_array.append(row)
            device = document
            #get data based on device_id
            cursor2 = collection.find_one({"flotta_egdedevice_id":device},sort=[( 'timestamp', pymongo.DESCENDING )]) 
            
            PredictionMade = ApiConfig.get_prediction(cursor2['temperature'], cursor2['humidity'],cursor2['soil_moisture'])
            row = {
                "flotta_egdedevice_id": device,
                "actual_soil_moisture": cursor2['soil_moisture'],
                "predicted_soil_moisture": PredictionMade
            }
            data_array.append(row)


        # json_data = json.dumps(data_array) 
        return Response(data_array, status=200)