import paho.mqtt.client as mqtt
from decouple import config
import json
import django
from monitor import apps

ApiConfig = apps.ApiConfig

def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    from .mqtt_functions import req_device_details, req_register_device

    decoded_message=str(msg.payload.decode("utf-8"))
    #check if decoded data can be converted to json 
    try:
        msg_json=json.loads(decoded_message)
        #if this is a request to a request made for the server
        if("flotta_egdedevice_id" in msg_json and "mqtt_request_for" in msg_json):
            if(msg_json['mqtt_request_for'] == "register_device"):
                print("SERVER: respond to register request")
                req_register_device(msg_json['flotta_egdedevice_id'], msg_json['device_type'], msg_json['raw_readings_type'], msg_json['raw_readings_units_type'])
                # requests.get('http://localhost:8000/api/devices/register/'+msg_json['flotta_egdedevice_id']+"/"+msg_json['device_type'])
            elif(msg_json['mqtt_request_for'] == "device_details"):
                print("SERVER: respond to user devices request")
                # requests.get('http://localhost:8000/api/devices/device/'+msg_json['flotta_egdedevice_id'])
                req_device_details(msg_json['flotta_egdedevice_id'])
    except ValueError as e:
       print("RECEIVED STRING VALUES: "+decoded_message)


    else:
        print("SERVER on_message: MQTT request does not have the parameters for API interaction")







