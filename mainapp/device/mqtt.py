import paho.mqtt.client as mqtt
from decouple import config
import json

#MQTT SUBSCTI
def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected mqtt successfully')
        mqtt_client.subscribe(config('MQTT_TOPIC'))
    else:
        print('Bad mqtt connection. Code:', rc)

client = mqtt.Client()
client.on_connect = on_connect
# client.on_message = on_message
client.username_pw_set(config('MQTT_USERNAME'), config('MQTT_PASSWORD'))
client.connect(
    host=config('MQTT_BROKER_ADDR'),
    port=int(config('MQTT_PORT'))
)
