import os
import joblib
from django.apps import AppConfig
from django.conf import settings
from pymongo import MongoClient


class ApiConfig(AppConfig):
    name = 'monitor'
    MODEL_FILE = os.path.join(settings.MODELS, "rrModel.joblib")
    model = joblib.load(MODEL_FILE)

    #INFLUXDB VARIABLES
    BUCKET = 'mqtt_bucket'
    ORG = 'primary'
    TOKEN = 'KzXHeJd-O0VzrnBOS9pnqKIxMZyvBALukcYlbmxCghsMqyPfvzp3OJhSJml8HRl60FssyTAFEED2NrY0JBUUxA=='
    URL ='http://192.168.13.204:8086'

    

    def get_mongo_database():
        MONGO_ADDR = '192.168.13.206:27017'

        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://username:password@"+MONGO_ADDR
        
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)
        
        # Create the database for our example (we will use the same database throughout the tutorial
        return client['mqtt_bucket']
    
    def get_prediction(temperature, humidity, soil_moisture):
        dtree = ApiConfig.model
        #predict using independent variables
        PredictionMade = dtree.predict([[temperature, humidity, soil_moisture]])

        return PredictionMade