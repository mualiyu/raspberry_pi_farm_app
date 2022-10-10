import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="192.168.43.134"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("test")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()
