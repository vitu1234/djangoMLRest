import paho.mqtt.client as mqtt
from decouple import config
import json
import django
from django.http import HttpRequest
import requests

if django.apps.registry.apps.ready:
    # The app registry is loaded and ready for use
    print("The app registry is ready")
    # Access information about the installed apps here
    # from .views import register_device


def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    decoded_message=str(msg.payload.decode("utf-8"))
    msg_json=json.loads(decoded_message)
    #if this is a request to a request made for the server
    if("flotta_egdedevice_id" in msg_json and "mqtt_request_for" in msg_json):
        if(msg_json['mqtt_request_for'] == "register_device"):
            print("respond to register request")
            requests.get('http://localhost:8000/api/devices/register/'+msg_json['flotta_egdedevice_id']+"/"+msg_json['device_type'])
        elif(msg_json['mqtt_request_for'] == "devices_details"):
            print("respond to user devices request")
            requests.get('http://localhost:8000/api/devices/device/'+msg_json['flotta_egdedevice_id'])
    else:
        print("MQTT request does not have the parameters for API interaction")






