from device import mqtt, my_mqtt
mqtt.client.on_message =my_mqtt.on_message
mqtt.client.loop_start()