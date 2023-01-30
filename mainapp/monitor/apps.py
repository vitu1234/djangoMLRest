import os
import random
import joblib
from django.apps import AppConfig
from django.conf import settings
from pymongo import MongoClient
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish

import json

class ApiConfig(AppConfig):
    name = 'monitor'
    MODEL_FILE = os.path.join(settings.MODELS, "rrModel.joblib")
    model = joblib.load(MODEL_FILE)

    #INFLUXDB VARIABLES
    BUCKET = 'mqtt_bucket'
    ORG = 'primary'
    TOKEN = 'KzXHeJd-O0VzrnBOS9pnqKIxMZyvBALukcYlbmxCghsMqyPfvzp3OJhSJml8HRl60FssyTAFEED2NrY0JBUUxA=='
    URL ='http://192.168.13.204:8086'

    #MQTT VARIABLES
    random_id = random.randint(100, 90000)
    BROKER = "192.168.13.203"
    TOPIC = "sensors/data"
    THIS_DEVICE = "API_SERVER"
    CLIENT_ID = THIS_DEVICE+str(random_id) # concatenate 4 numbers to uniquely identify this device
    PORT = 1883
    

    def get_mongo_database():
        MONGO_ADDR = '192.168.13.206:27017'

        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://username:password@"+MONGO_ADDR
        
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)
        
        # Create the database for our example (we will use the same database throughout the tutorial
        return client['mqtt_bucket']

   #get predictions from the ML model 
    def get_prediction(temperature, humidity, soil_moisture):
        dtree = ApiConfig.model
        #predict using independent variables
        PredictionMade = dtree.predict([[temperature, humidity, soil_moisture]])
        
        return PredictionMade
    
    #connect to mqtt
    def connect_mqtt() -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        client = mqtt_client.Client(ApiConfig.CLIENT_ID)
        client.username_pw_set("mqtt", "mqtt")
        client.on_connect = on_connect
        client.connect(ApiConfig.BROKER, ApiConfig.PORT)
        return client
    
    #publish to mqtt topic
    def publish_mqtt(client, pump_flotta_egdedevice_id, pump_action):
            
        device_id = pump_flotta_egdedevice_id
        data = {
            "pump_flotta_egdedevice_id": device_id,
            "pump_action": pump_action
        }
        payload = json.dumps(data)
        result =client.publish(ApiConfig.TOPIC, payload)
        client.disconnect()
        # result: [0, 1]
        status = result[0]
        if status == 0:
            return 1 #published to topic
        else:
            return 0 #failed to publish to topic

