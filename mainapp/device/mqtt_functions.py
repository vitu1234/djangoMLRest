
from decouple import config
import json
from monitor import apps
from .mqtt import client as my_mqtt_client



ApiConfig = apps.ApiConfig


#get device details

def req_device_details(flotta_egdedevice_id):
    database = ApiConfig.get_mongo_database()
    print("DEVDE")
    collection = database["devices"]
    cursor = collection.find_one({"flotta_egdedevice_id":flotta_egdedevice_id})
    # return Response("cursor", status=200)
    print(cursor)
    devices_details = [] 
    if len(cursor) !=0:
        
        row = {
            "flotta_egdedevice_id": cursor['flotta_egdedevice_id'],
            "user_claim": cursor['user_claim'],
            "mode": cursor['mode'],
            "device_type": cursor['device_type'],
        }
        
        if cursor['device_type'] =="sensor" and cursor['user_claim']:
            raw_readings_type_list =  (((cursor['columns_readings_type'].lower()).strip()).replace(" ", "")).split(",") #lower case,remove commas and spaces and covert to array
            row['columns']=raw_readings_type_list
        
        devices_details.append(row)
        
        data_array = {
            "error":False, 
            "msg":"Device Details",
            "device_id": flotta_egdedevice_id,
            "mqtt_response_for":"devices_details",
            "devices_details": devices_details
        }
        #add mqtt publish
        payload = json.dumps(data_array)
        result = my_mqtt_client.publish(config('MQTT_TOPIC'), payload)
        status_mqtt = result[0]
        if status_mqtt == 0:
            print("DEVICE DETAILS: Published to MQTT BROKER: "+config('MQTT_BROKER_ADDR')+"on PORT: "+config('MQTT_PORT'))
        else:
            print("DEVICE DETAILS: Failed published to MQTT BROKER: "+config('MQTT_BROKER_ADDR')+"on PORT: "+config('MQTT_PORT'))
        
        return data_array
    else:
        print("H")
        return {"error": True, "msg":"No device device with given parameter"}

#check if device exists or register in
def req_register_device(flotta_egdedevice_id,device_type):
    print("RESPONSE")
    database = ApiConfig.get_mongo_database()
    collection = database["devices"]
    cursor = collection.find_one({"flotta_egdedevice_id":flotta_egdedevice_id})
    print(cursor)
    if len(cursor) != 0:
        newdevice = {
            'flotta_egdedevice_id':flotta_egdedevice_id,
            'user_claim':False,
            'mode':'Auto',
            'device_type': device_type
        }
        collection.insert_one(newdevice)
        data_array = {
            "error":False, 
            "msg":"success",
            "device_id": flotta_egdedevice_id,
            "mqtt_response_for":"register_device",
        }
        #add mqtt publish
        payload = json.dumps(data_array)
        result = my_mqtt_client.publish(config('MQTT_TOPIC'), payload)
        status_mqtt = result[0]
        if status_mqtt == 0:
            print("Published to MQTT BROKER: "+config('MQTT_BROKER_ADDR')+"on PORT: "+config('MQTT_PORT'))
        else:
            print("Failed published to MQTT BROKER: "+config('MQTT_BROKER_ADDR')+"on PORT: "+config('MQTT_PORT'))
        
        return False
    else:
        print("YO")
        return False

